from dash import html
import utils

def handle_display_styles(isocyanate_clicks, hydroxyl_clicks, make_oligomer_clicks, size_value, all_isocyanate, all_hydroxyl, isocyanate_value, hydroxyl_values, contents, file_content, capping_group, isocyanate_all, hydroxyl_all):
    
    valid_file = "Accepted input file content: Name;SMILES"
    
    right_panel_style = {'display': 'flex'}
    
    if isocyanate_clicks and hydroxyl_clicks and make_oligomer_clicks == 0 :
        
        hydroxyl_list_style = {'flex': '1', 'padding': '10px', 'display':'block'}
        isocyanate_list_style = {'flex': '1', 'padding': '10px', 'display':'block'}
        reaction_output_children = []
        left_panel_before_style = {'display': 'block'}
        left_panel_after_children = []
        successful_upload_children = [valid_file]
        left_panel_download_style = {'display':'none'}
        store_reaction_data = []
    
    elif isocyanate_clicks and make_oligomer_clicks == 0 :
        
        hydroxyl_list_style = {'flex': '1', 'padding': '10px', 'display':'none'}
        isocyanate_list_style = {'flex': '1', 'padding': '10px', 'display':'block'}
        reaction_output_children = []
        left_panel_before_style = {'display': 'block'}
        left_panel_after_children = []
        successful_upload_children = [valid_file]
        left_panel_download_style = {'display':'none'}
        store_reaction_data = []
    
    elif hydroxyl_clicks and make_oligomer_clicks == 0 :
        
        hydroxyl_list_style = {'flex': '1', 'padding': '10px', 'display':'block'}
        isocyanate_list_style = {'flex': '1', 'padding': '10px', 'display':'none'}
        reaction_output_children = []
        left_panel_before_style = {'display': 'block'}
        left_panel_after_children = []
        successful_upload_children = [valid_file]
        left_panel_download_style = {'display':'none'}
        store_reaction_data = []
    
    elif make_oligomer_clicks == 0:
        if contents is not None:
            if file_content:
                lines = file_content.splitlines()
                
                if lines:
                    if lines[0] == 'Name;SMILES':
                        line_num = range(1, len(lines))
                    else:
                        line_num = range(len(lines))
                    
                    smiles = isocyanate_value + hydroxyl_values    
                    for l in line_num:
                        if lines[l] != "":
                            try:
                                comp = lines[l].split(";")
                                valid_smiles = utils.is_valid_smiles(comp[1])
                                if not valid_smiles:
                                    valid_file = "Compounds in SMILES not detected."
                                    break
                                else:
                                    if comp[1] not in smiles:
                                        smiles.append(comp[1])
                                    valid_file = "File is uploaded."
                            except:
                                valid_file = "Wrong file format."
                            
                else:
                    valid_file = "File is empty or wrong file format."
                                
            else:
                valid_file = "File is empty or wrong file format."
                        
        hydroxyl_list_style = {'flex': '1', 'padding': '10px', 'display':'none'}
        isocyanate_list_style = {'flex': '1', 'padding': '10px', 'display':'none'}
        reaction_output_children = [html.Img(src='assets/purge_main.png', style={'max-width': '100%', 'height': 'auto'})]
        left_panel_before_style = {'display': 'block'}
        left_panel_after_children = []
        successful_upload_children = [valid_file]
        left_panel_download_style = {'display':'none'}
        store_reaction_data = []
    
    elif make_oligomer_clicks: 
        
        if all_hydroxyl and all_isocyanate:
            smiles = isocyanate_all + hydroxyl_all
        
        elif all_hydroxyl and not all_isocyanate:
            smiles = isocyanate_value + hydroxyl_all
            
        elif all_isocyanate and not all_hydroxyl:
            smiles = isocyanate_all + hydroxyl_values        
        else:
            smiles = isocyanate_value + hydroxyl_values
            
        
        if file_content:
            lines = file_content.splitlines()
            
            if lines[0] == 'Name;SMILES':
                line_num = range(1, len(lines))
            else:
                line_num = range(len(lines))
                
            for l in line_num:
                if lines[l] != "":
                    comp = lines[l].split(";")
                    valid_smiles = utils.is_valid_smiles(comp[1])
                    if not valid_smiles:
                        break
                    else:
                        if comp[1] not in smiles:
                            smiles.append(comp[1])
                        

        if smiles:
            reaction, info, iso_mols, poliol_mols = utils.prepare_reaction(smiles)
            
            if reaction:
                reaction_output = "PERFORMED REACTIONS"
                if not capping_group:
                    capping_group="-N=C=O"
                
                if size_value == "2":
                    
                    reagents_smiles, products_smiles = utils.perform_dimerization(iso_mols,poliol_mols)
                    
                    capped_products = [utils.modify_molecule(product, capping_group[1:]) for product in products_smiles]
                    
                    reactions = html.Div(
                        [
                            
                            html.Div([
                                
                                html.H4(["Reaction %i: "%(i+1)],style={'font-weight': 'bold', 'margin-left': '20px', 'margin-top': '-15px', 'margin-bottom':'0',
                                                                       'color': '#555',
                                                                        'font-size': '15px',
                                                                        'font-weight': '600',
                                                                        'letter-spacing': '.1rem',
                                                                        'text-transform': 'uppercase',
                                                                        'text-decoration': 'none',
                                                                        'white-space': 'nowrap'}),
                                html.Img(src='data:image/jpeg;base64,' + utils.smiles_to_image(reagents_smiles[i][0]), 
                                style={'height': '150px','width':'auto', 'margin': '0'}),
                                html.Img(src='assets/plus.png', 
                                style={'height': '10px','width':'auto', 'margin-bottom': '80px'}),
                                html.Img(src='data:image/jpeg;base64,' + utils.smiles_to_image(reagents_smiles[i][1]), 
                                style={'height': '150px','width':'auto', 'margin': '0'}),
                                
                                html.Img(src='assets/arrow.png',
                                style={'height': '20px','width':'auto', 'margin-bottom': '75px'}),
                                html.Img(src='data:image/jpeg;base64,' + utils.smiles_to_image(product), 
                                style={'height': '150px','width':'auto', 'margin': '0'}),
                                 
                            ])
                            for i,product in enumerate(capped_products)
                        
                        ]
                    )
                    
                elif size_value == "3":
                    
                    reagents_smiles, products_smiles = utils.perform_trimerization(iso_mols,poliol_mols)
                    
                    capped_products = [utils.modify_molecule(product, capping_group[1:]) for product in products_smiles]
                    
                    reactions = html.Div(
                        [
                            
                            html.Div([
                                
                                html.H4(["Reaction %i: "%(i+1)],style={'font-weight': 'normal', 'margin-left': '20px', 'margin': '0'}),
                                html.Img(src='data:image/jpeg;base64,' + utils.smiles_to_image(reagents_smiles[i][0]), 
                                style={'height': '150px','width':'auto', 'margin': '0'}),
                                html.Img(src='assets/plus.png', 
                                style={'height': '10px','width':'auto', 'margin-bottom': '80px'}),
                                html.Img(src='data:image/jpeg;base64,' + utils.smiles_to_image(reagents_smiles[i][1]), 
                                style={'height': '150px','width':'auto', 'margin': '0'}),
                                html.Img(src='assets/plus.png', 
                                style={'height': '10px','width':'auto', 'margin-bottom': '80px'}),
                                html.Img(src='data:image/jpeg;base64,' + utils.smiles_to_image(reagents_smiles[i][2]), 
                                style={'height': '150px','width':'auto', 'margin': '0'}),
                                
                                html.Img(src='assets/arrow.png',
                                style={'height': '20px','width':'auto', 'margin-bottom': '75px'}),
                                html.Img(src='data:image/jpeg;base64,' + utils.smiles_to_image(product), 
                                style={'height': '150px','width':'auto', 'margin': '0'}),
                                 
                            ])
                            for i,product in enumerate(capped_products)
                        
                        ]
                    )
                
                if size_value == "4":
                    
                    reagents_smiles, products_smiles = utils.perform_tetramerization(iso_mols,poliol_mols)
                    
                    capped_products = [utils.modify_molecule(product, capping_group[1:]) for product in products_smiles]
                    
                    reactions = html.Div(
                        [
                            
                            html.Div([
                                
                                html.H4(["Reaction %i: "%(i+1)],style={'font-weight': 'normal', 'margin-left': '20px', 'margin': '0'}),
                                html.Img(src='data:image/jpeg;base64,' + utils.smiles_to_image(reagents_smiles[i][0]), 
                                style={'height': '150px','width':'auto', 'margin': '0'}),
                                html.Img(src='assets/plus.png', 
                                style={'height': '10px','width':'auto', 'margin-bottom': '80px'}),
                                html.Img(src='data:image/jpeg;base64,' + utils.smiles_to_image(reagents_smiles[i][1]), 
                                style={'height': '150px','width':'auto', 'margin': '0'}),
                                html.Img(src='assets/plus.png', 
                                style={'height': '10px','width':'auto', 'margin-bottom': '80px'}),
                                html.Img(src='data:image/jpeg;base64,' + utils.smiles_to_image(reagents_smiles[i][2]), 
                                style={'height': '150px','width':'auto', 'margin': '0'}),
                                html.Img(src='assets/plus.png', 
                                style={'height': '10px','width':'auto', 'margin-bottom': '80px'}),
                                html.Img(src='data:image/jpeg;base64,' + utils.smiles_to_image(reagents_smiles[i][3]), 
                                style={'height': '150px','width':'auto', 'margin': '0'}),
                                
                                html.Img(src='assets/arrow.png',
                                style={'height': '20px','width':'auto', 'margin-bottom': '75px'}),
                                html.Img(src='data:image/jpeg;base64,' + utils.smiles_to_image(product), 
                                style={'height': '150px','width':'auto', 'margin': '0'}),
                                 
                            ])
                            for i,product in enumerate(capped_products)
                        
                        ]
                    )
                               
            else:
                reaction_output = """Reactions can't be performed with selected substrates.
                                    Make sure there is at least one hydroxyl compound and one isocyanate."""
                reactions = ""
                capped_products = ""
            
            
            
        else:
            info = "Select substrates!"

        
        hydroxyl_list_style = {'flex': '1', 'padding': '10px', 'display':'none'}
        isocyanate_list_style = {'flex': '1', 'padding': '10px', 'display':'none'}
        reaction_output_children = [html.Img(src='assets/purge_reaction.png', style={'max-width': '100%', 'height': 'auto'}),
                                    html.Div([html.Div('SUMMARY', style={'margin-bottom':'10px', 'margin-top': '-50px', 'margin-left':'20px', 'font-weight':'bold', 'font-size':'18px', 'opacity':'0.6'}),
                                              html.Div('Number of uploaded substrates: %i'%info[0], style={'margin-bottom':'10px', 'margin-top': '10px', 'margin-left':'20px'}),
                                              html.Div('Substrates types:', style={'margin-left':'20px'}),
                                              html.Div('%i isocyanates'%info[1], style={'margin-left':'30px'}),
                                              html.Div('%i diisocyanates'%info[2], style={'margin-left':'30px'}),
                                              html.Div('%i alcohols/phenols'%info[3], style={'margin-left':'30px'}),
                                              html.Div('%i diols'%info[4], style={'margin-left':'30px'}) ], 
                                             style = {'color': '#555',
                                                      'text-align': 'left',
                                                      'font-size': '16px',
                                                      'font-weight': '600',
                                                      'line-height': '25px',
                                                      'letter-spacing': '.1rem',
                                                      'text-transform': 'uppercase',
                                                      'text-decoration': 'none',
                                                      'font-weight': 'normal',
                                                      'white-space': 'nowrap'}),
                                    html.H2([reaction_output], style = {'font-weight': 'normal', 
                                                                        'text-align': 'center'}),
                                    html.Div(reactions)]
        left_panel_before_style = {'display': 'none'}
        left_panel_after_children = [html.A(html.Button('Main page'),
                                            href='/', 
                                            style={'opacity':'0.9', 
                                                   'border-radius': '1px', 
                                                   'margin-left':'5px'}),
                                     html.H2(["%i GENERATED STRUCTURES" %(len(products_smiles))], 
                                             style = {'font-weight': 'bold', 
                                                      'margin-top': '50px',
                                                      'margin-bottom':'20px',
                                                      'text-align': 'center',
                                                      'color': '#555',
                                                      'font-size': '18px',
                                                      'font-weight': '600',
                                                      'line-height': '18px',
                                                      'letter-spacing': '.1rem',
                                                      'text-transform': 'uppercase',
                                                      'text-decoration': 'none',
                                                      'white-space': 'nowrap'})]
        successful_upload_children = []
        left_panel_download_style = {'display':'block'}
        store_reaction_data = capped_products
        
    return right_panel_style, hydroxyl_list_style, isocyanate_list_style, reaction_output_children, left_panel_before_style, left_panel_after_children, successful_upload_children, left_panel_download_style, store_reaction_data
