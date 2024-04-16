from dash import html
import utils
import base64

def validate_input_file(contents, filename):
    uploaded_substrates = []
    if filename:
        if contents:
            decoded_content = base64.b64decode(contents.split(",")[1]).decode('utf-8')
            lines = decoded_content.splitlines()
            if lines:
                if lines[0] == 'Name;SMILES':
                    line_num = range(1, len(lines))
                else:
                    line_num = range(len(lines))
                
                for l in line_num:
                    if lines[l] != "":
                        try:
                            comp = lines[l].split(";")
                            uploaded_substrates.append(comp[1])
                            valid_smiles = utils.is_valid_smiles(comp[1])
                            if not valid_smiles:
                                valid_file = "Compounds in SMILES not detected."
                                break
                            else:
                                valid_file = f"{filename} is uploaded."
                        except:
                            valid_file = f"{filename} - wrong file format."
            else:
                valid_file = f"{filename} is empty or wrong file format."                        
        else:
            valid_file = f"{filename} is empty."
    else:
        valid_file = ""
    return valid_file, uploaded_substrates

def show_reactions(smiles, size_value, capping_group):
    if smiles:
        reaction, info, iso_mols, poliol_mols = utils.prepare_reaction(smiles)
        
        if reaction:
            
            if not capping_group:
                        capping_group="-N=C=O"
            if size_value == "2":
                    
                reagents_smiles, products_smiles = utils.perform_dimerization(iso_mols,poliol_mols)
                
                capped_products = [utils.modify_molecule(product, capping_group[1:]) for product in products_smiles]
                
                
            elif size_value == "3":
                
                reagents_smiles, products_smiles = utils.perform_trimerization(iso_mols,poliol_mols)
                
                capped_products = [utils.modify_molecule(product, capping_group[1:]) for product in products_smiles]
            
            if size_value == "4":
                
                reagents_smiles, products_smiles = utils.perform_tetramerization(iso_mols,poliol_mols)
                
                capped_products = [utils.modify_molecule(product, capping_group[1:]) for product in products_smiles]
            
            products_imgs = html.Div(
                    [
                        html.Div([
                            
                            html.H4([f"Compound {i+1}"],style={'font-weight': 'normal', 'margin-left': '20px'}),
                            html.Img(src='data:image/jpeg;base64,' + utils.smiles_to_image(product), 
                            style={'height': '250px','width':'auto', 'margin': '30'}),
                                
                        ])
                        for i,product in enumerate(capped_products)
                    ], style={
            'display': 'flex',
            'flex-wrap': 'wrap',
            'justify-content': 'flex-start',  # Align items to the left
            'margin-top': '20px'  # Add some margin between rows
        }
                )

        else:
            products_imgs = ""
            capped_products = ""
        
        
        
    else:
        info = "Select substrates!"

    summary = [
        html.Div([
                html.Div(f'Number of uploaded substrates: {info[0]}', style={'margin-bottom':'10px', 'margin-top': '10px', 'margin-left':'20px'}),
                html.Div('Substrates types:', style={'margin-left':'20px'}),
                html.Div(f'{info[1]} isocyanates', style={'margin-left':'30px'}),
                html.Div(f'{info[2]} diisocyanates', style={'margin-left':'30px'}),
                html.Div(f'{info[3]} alcohols/phenols', style={'margin-left':'30px'}),
                html.Div(f'{info[4]} diols', style={'margin-left':'30px'}), 
                html.Div(f'Isocyanate capping group: {capping_group}', style={'margin-left':'20px', 'margin-top': '10px'}),
                html.Div(f'Selected size: {size_value} units', style={'margin-left':'20px', 'margin-top': '10px'}),
                html.Div(f'Number of generated PUR fragments: {len(capped_products)}', style={'margin-left':'20px', 'margin-top': '20px'}),
                ],
                className='summary-text')]
    
    structures_imgs =[html.Div(products_imgs)]
    return summary, structures_imgs, capped_products
