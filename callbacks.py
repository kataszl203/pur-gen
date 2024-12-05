from typing import Tuple

from dash import html
import utils
import base64

ALLOWED_EXTENSIONS = {'txt', 'csv'}  # Define the allowed file extensions

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_input_file(contents, filename):
    uploaded_substrates = []
    
    if not filename:
        return "", uploaded_substrates
    
    if not allowed_file(filename):
        return f"{filename} has an invalid file extension. Only .txt and .csv are allowed.", uploaded_substrates
    
    if not contents:
        return f"{filename} is empty.", uploaded_substrates
    
    decoded_content = base64.b64decode(contents.split(",")[1]).decode('utf-8')
    lines = decoded_content.splitlines()
    
    if not lines:
        return f"{filename} is empty or wrong file format.", uploaded_substrates
    
    if lines[0] != 'Name;SMILES':
        start_index = 0
    else:
        start_index = 1
    
    for line in lines[start_index:]:
        if line == "":
            continue
        
        try:
            name, smiles = line.split(";")
            uploaded_substrates.append(smiles)
            if not utils.is_valid_smiles(smiles):
                return "Compounds in SMILES not detected.", uploaded_substrates
        except ValueError:
            return f"{filename} - wrong file format.", uploaded_substrates
    
    return f"{filename} is uploaded.", uploaded_substrates


def validate_text_input(contents: str) -> Tuple[str, list, bool, list]:
    uploaded_substrates = []
    incorrect_smiles = []
    return_string: str = f""

    if not contents or contents=="":
        return f"Input is empty.", uploaded_substrates, False, []

    lines = contents.splitlines()

    if not lines:
        return "Input is empty or in the wrong format.", uploaded_substrates, False, []

    if lines[0] != 'Name;SMILES':
        start_index = 0
    else:
        start_index = 1

    for line in lines[start_index:]:
        if line == "":
            continue

        try:
            name, smiles = line.split(";")
            if not utils.is_valid_smiles(smiles):
                incorrect_smiles.append(f"{name}: {smiles}")
                return_string += f"Compounds in SMILES not detected for line: \n\"{line}\".\n\n"
                continue
            uploaded_substrates.append(smiles)
        except ValueError:
            return_string += f"Wrong input format in line: \n\"{line}\".\n\n"
            continue

    return return_string+f"Input has been loaded.", uploaded_substrates, True, incorrect_smiles

def show_reactions(smiles, size_value, capping_group=None):
    summary = ""
    structures_imgs = ""
    capped_products = ""
    
    if not smiles:
        return summary, structures_imgs, capped_products
    
    reaction, info, iso_mols, poliol_mols, not_classified_smiles = utils.prepare_reaction(smiles)
    
    if not reaction:
        return summary, structures_imgs, capped_products
    
    if not capping_group:
        capping_group = "-N=C=O"

    if size_value == "2": 
        products_smiles = utils.perform_dimerization(iso_mols, poliol_mols)               

    elif size_value == "3":
        products_smiles = utils.perform_trimerization(iso_mols, poliol_mols)               

    elif size_value == "4":
        products_smiles = utils.perform_tetramerization(iso_mols, poliol_mols)               

    capped_products = [utils.modify_molecule(product, capping_group[1:]) for product in products_smiles]
    
    products_imgs = html.Div([html.Div([
                html.H4(f"Compound {i+1}", style={'font-weight': 'normal', 'margin-left': '20px'}),
                html.Img(src='data:image/jpeg;base64,' + utils.smiles_to_image(product), 
                         style={'height': '250px','width':'auto', 'margin': '30'}),
            ])
            for i, product in enumerate(capped_products)
        ], className = 'products-list')

    summary = html.Div([
        html.Div(f'Number of uploaded substrates: {info[0]}', style={'margin-bottom':'10px', 'margin-top': '10px', 'margin-left':'20px'}),
        html.Div('Substrates types:', style={'margin-left':'20px'}),
        html.Div(f'{info[1]} monoisocyanates', style={'margin-left':'30px'}),
        html.Div(f'{info[2]} diisocyanates', style={'margin-left':'30px'}),
        html.Div(f'{info[3]} monohydroxy alcohols', style={'margin-left':'30px'}),
        html.Div(f'{info[4]} diols', style={'margin-left':'30px'}), 
        html.Div(f'Isocyanate capping group: {capping_group}', style={'margin-left':'20px', 'margin-top': '10px'}),
        html.Div(f'Selected size: {size_value} units', style={'margin-left':'20px', 'margin-top': '10px'}),
        html.Div(f'Number of generated PUR fragments: {len(capped_products)}', style={'margin-left':'20px', 'margin-top': '20px'}),
        html.Button('DOWNLOAD GENERATED DATA', id='download-generated-data', n_clicks=0, style={
            'width': '500px', "margin-top": "20px"
        }),
        # html.Div(f"This website uses Open Babel to generate up to 20 conformers. However, due to its limitations, larger or more complex compounds from PUR-GEN may produce fewer conformers, sometimes only one structure. If needed, we recommend trying other conformer generation tools, such as : ", className="box"),
        # html.A('Mobyle@RPBS', href='https://mobyle2.rpbs.univ-paris-diderot.fr/', target='_blank', className="link-box")
    ], className='summary-text')
    
    structures_imgs = [html.Div(products_imgs)]
    
    return summary, structures_imgs, capped_products
