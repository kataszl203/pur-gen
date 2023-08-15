from rdkit import Chem
from rdkit.Chem import Draw, AllChem
from rdkit.Chem import rdChemReactions
from openbabel import openbabel as ob
from openbabel import pybel
import io
import base64

# General settings
conformer = ob.OBConformerSearch()
conformer.SetLogStream(None)
x = ob.OBMinimizingEnergyConformerScore()
conformer.SetScore(x)
y = ob.OBStericConformerFilter()
conformer.SetFilter(y)
pff = ob.OBForceField_FindType("gaff")

# Substrates properties
iso = Chem.MolFromSmiles('N=C=O')
diiso = Chem.MolFromSmiles('O=C=N.N=C=O')
ol = Chem.MolFromSmiles('CO')
ol_2 = Chem.MolFromSmiles('COCCO')
diol = Chem.MolFromSmiles('OC.CO')

# Reactions in SMARTS
# Dimerization
ab = '[N:1]=[C:2]=[O:3].[C:4][O;H1:5]>>[N:1][C:2]([O:5][C:4])=[O:3]'
# Trimerization
aba = '[N:1]=[C:2]=[O:3].([O;H1:4][C:5].[C:6][O;H1:7]).[N:8]=[C:9]=[O:10]>>([N:1][C:2](=[O:3])[O:4][C:5].[C:6][O:7][C:9](=[O:10])[N:8])'
bab = '[C:1][O;H1:2].([O:3]=[C:4]=[N:5].[N:6]=[C:7]=[O:8]).[C:9][O;H1:10]>>([C:1][O:2][C:4](=[O:3])[N:5].[N:6][C:7](=[O:8])[O:10][C:9])'
# Tetramerization
abab = ('[N:1]=[C:2]=[O:3].([O;H1:4][C:5].[C:6][O;H1:7]).([N:8]=[C:9]=[O:10].[N:11]=[C:12]=[O:13]).[O;H1:14][C:15]>>'
        '([N:1][C:2](=[O:3])[O:4][C:5].[C:6][O:7][C:9](=[O:10])[N:8].[N:11][C:12](=[O:13])[O:14][C:15])')


def is_valid_smiles(smiles):
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return False
        return True
    except:
        return False

def pil_to_base64(pil_img):
    buffered = io.BytesIO()
    pil_img.save(buffered, format="JPEG")  # Use the appropriate format here (JPEG, PNG, etc.)
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return img_str

def smiles_to_image(input_smiles):
    m = Chem.MolFromSmiles(input_smiles)
    pil_img = Draw.MolToImage(m)
    img_str = pil_to_base64(pil_img)
    return img_str

def prepare_reaction(smiles):
  
    substrates_mols = []
    for substrate in smiles:
        mol = Chem.MolFromSmiles(substrate)
        substrates_mols.append(mol)

    ## New
    iso_mols = []  # isocyanates and diisocyanates
    poliol_mols = []  # mono and poliols

    # Assign properties to the substrates according to the functional group
    n_diiso = 0
    n_iso = 0
    n_ol = 0
    n_diol = 0
    n = 0
    for comp in substrates_mols:
        if comp.HasSubstructMatch(diiso):
            comp.SetProp('func_group', 'diiso')
            iso_mols.append(comp)
            n_diiso += 1

        elif comp.HasSubstructMatch(iso):
            comp.SetProp('func_group', 'iso')
            iso_mols.append(comp)
            n_iso += 1

        elif comp.HasSubstructMatch(diol):
            if comp.HasSubstructMatch(ol_2):
                comp.SetProp('func_group', 'ol')
                poliol_mols.append(comp)
                n_ol += 1
            else:
                comp.SetProp('func_group', 'diol')
                poliol_mols.append(comp)
                n_diol += 1

        elif comp.HasSubstructMatch(ol):
            comp.SetProp('func_group', 'ol')
            poliol_mols.append(comp)
            n_ol += 1

        
        n += 1

    info = [n, n_iso, n_diiso, n_ol, n_diol]
    
    return (n_iso != 0 or n_diiso != 0) and (n_ol != 0 or n_diol != 0), info, iso_mols, poliol_mols


def perform_dimerization(a_list, b_list):
    reagents_smiles = []
    products_smiles = []
    products_list = []

    for a in a_list:
        for b in b_list:
            reaction = ab
            reacts = (a, b)
            rxn = rdChemReactions.ReactionFromSmarts(reaction)
            products = rxn.RunReactants(reacts)
            products_list.append(products[0][0])
            reagents_smiles.append([Chem.MolToSmiles(reacts[0]), Chem.MolToSmiles(reacts[1])])
            products_smiles.append(Chem.MolToSmiles(products[0][0]))
    return reagents_smiles, products_smiles


def perform_trimerization(a_list, b_list):
    reagents_smiles = []
    products_smiles = []
    products_list = []

    for a in a_list:
        for b in b_list:
            
            reaction1 = bab
            reaction2 = aba
            reacts1 = (b, a, b)
            reacts2 = (a, b, a)
            rxn1 = rdChemReactions.ReactionFromSmarts(reaction1)
            rxn2 = rdChemReactions.ReactionFromSmarts(reaction2)
                
            if a.GetProp('func_group') == 'iso' and b.GetProp('func_group') == 'diol':
                products = rxn2.RunReactants(reacts2)
                products_list.append(products[0][0])
                reagents_smiles.append(
                    [Chem.MolToSmiles(reacts2[0]), Chem.MolToSmiles(reacts2[1]), Chem.MolToSmiles(reacts2[2])])
                products_smiles.append(Chem.MolToSmiles(products[0][0]))

            elif a.GetProp('func_group') == 'diiso' and b.GetProp('func_group') == 'ol':
                products = rxn1.RunReactants(reacts1)
                products_list.append(products[0][0])
                reagents_smiles.append(
                    [Chem.MolToSmiles(reacts1[0]), Chem.MolToSmiles(reacts1[1]), Chem.MolToSmiles(reacts1[2])])
                products_smiles.append(Chem.MolToSmiles(products[0][0]))
            
            elif a.GetProp('func_group') == 'diiso' and b.GetProp('func_group') == 'diol':
                products1 = rxn1.RunReactants(reacts1)
                products_list.append(products1[0][0])
                reagents_smiles.append(
                    [Chem.MolToSmiles(reacts1[0]), Chem.MolToSmiles(reacts1[1]), Chem.MolToSmiles(reacts1[2])])
                products_smiles.append(Chem.MolToSmiles(products1[0][0]))
                
                products2 = rxn2.RunReactants(reacts2)
                products_list.append(products2[0][0])
                reagents_smiles.append(
                    [Chem.MolToSmiles(reacts2[0]), Chem.MolToSmiles(reacts2[1]), Chem.MolToSmiles(reacts2[2])])
                products_smiles.append(Chem.MolToSmiles(products2[0][0]))
                

    return reagents_smiles, products_smiles


def perform_tetramerization(a_list, b_list):
    reagents_smiles = []
    products_smiles = []
    products_list = []

    for a in a_list:
        if a.GetProp('func_group') == 'diiso':
            for b in b_list:
                if b.GetProp('func_group') == 'diol':
                    reaction = abab
                    reacts = (a, b, a, b)
                    rxn = rdChemReactions.ReactionFromSmarts(reaction)
                    products = rxn.RunReactants(reacts)
                    products_list.append(products[0][0])
                    reagents_smiles.append(
                        [Chem.MolToSmiles(reacts[0]), Chem.MolToSmiles(reacts[1]), Chem.MolToSmiles(reacts[2]),
                         Chem.MolToSmiles(reacts[3])], )
                    products_smiles.append(Chem.MolToSmiles(products[0][0]))

    return reagents_smiles, products_smiles

def modify_molecule(smiles, condition):
    replacement = ""
    if condition == "CH3":
        # Replace NCO group with CH3
        replacement = '[CH3]'
    elif condition == "NH2":
        # Replace NCO group with NH2
        replacement = '[NH2]'
    elif condition == "NC(=O)OH":
        # Replace NCO group with NCOOH
        replacement = '[NX3][CX3](=[OX1])[OX2H0]'
    elif condition == "N=C=O":
        # Do nothing (leave NCO)
        return smiles
    new_mol = AllChem.ReplaceSubstructs(Chem.MolFromSmiles(smiles), Chem.MolFromSmarts('N=C=O'), Chem.MolFromSmarts(replacement), True)
    
    return Chem.MolToSmiles(new_mol[0])

def generate_mol(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is not None:
        mol_block = Chem.MolToMolBlock(mol)
        return mol_block
    
def generate_mol2(smiles, idx):
    conversion = ob.OBConversion()
    obmol = ob.OBMol()
    conversion.SetInAndOutFormats("smi", "mol2")
    gen3d = ob.OBOp.FindType("gen3D")
    conversion.ReadString(obmol, smiles)
    gen3d.Do(obmol, "--best")
    pybel.Molecule(obmol).title = f"PU_{idx + 1}"
    mol2_content = conversion.WriteString(obmol)
    return mol2_content

def generate_conformers(smiles, idx):
    num_conformers = 20
    conversion = ob.OBConversion()
    conversion.SetInAndOutFormats("smi", "mol2")
    
    conformers_content = []
    
    mol = pybel.readstring("smi", smiles)
    mol.addh()
    mol.make3D()
    pff.Setup(mol.OBMol)
    pff.DiverseConfGen(0.5, 1000000, 50.0, False)
    pff.GetConformers(mol.OBMol)
    if mol.OBMol.NumConformers() <= num_conformers:
        num_conformers = mol.OBMol.NumConformers()
    
    for j in range(num_conformers):
        mol.OBMol.SetConformer(j)
        pybel.Molecule(mol.OBMol).title = f"PU_{idx + 1}_{j}"
        conformers_content.append(conversion.WriteString(mol.OBMol))
    
    return conformers_content

def generate_image(smiles):
    mol = Chem.MolFromSmiles(smiles)  
    image = Chem.Draw.MolToImage(mol, size=(500, 500))
    image_buffer = io.BytesIO()
    image.save(image_buffer, format='PNG')
    image_content = image_buffer.getvalue()
    
    return image_content
