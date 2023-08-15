import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import dash_daq as daq
import flask
import io
import MakeOligomers_dash
from PIL import Image
import io
import base64
import zipfile
from flask import Flask, send_file
from io import BytesIO

external_stylesheets = ['assets/style.css']


# Create the Dash app
f_app = flask.Flask(__name__)
app = dash.Dash(__name__)

isocyanate_list = [{'label' : i.split(";")[0], 'smiles' : i.split(";")[1]} for i in open("assets/isocyanates.txt", "r").read().splitlines()]
hydroxyl_list = [{'label' : i.split(";")[0], 'smiles' : i.split(";")[1]} for i in open("assets/poliols.txt", "r").read().splitlines()]

def create_checkbox_list(options, table_title, table_id, checklist_id):
    return html.Div(
        style={'flex': '1', 'padding': '10px', 'display':'none'},
        id = table_id,
        children = [
            html.H3(table_title, style={'text-align': 'left'}),
            
            dcc.Checklist(
                id = checklist_id,
                options = [{
                    'label': html.Div([
                    html.H4([option['label']], style={'display': 'block','font-weight': 'normal','margin-left': '25px', 'margin-top':'-20px'}),
                    html.Img(src='data:image/jpeg;base64,' + MakeOligomers_dash.smiles_to_image(option['smiles']), 
                             style={'height': '200px','width':'auto', 'margin': '0'}),
                    ]),
                    'value': option['smiles']
                    } for option in options],
                value=[],)
        ])
    
checkbox_list_hydroxyl = create_checkbox_list(hydroxyl_list, "Select hydroxyl compounds:", 'hydroxyl-list', 'hydroxyl-list-checkbox')
checkbox_list_isocyanate = create_checkbox_list(isocyanate_list, "Select isocyanates: ", 'isocyanate-list', 'isocyanate-list-checkbox')

# Define the layout of the app
app.layout = html.Div(
    style={'display': 'flex', 'font-family': 'Calibri'},
    children=[
    html.Div(id = 'left-panel-content', 
             style = {'flex': '1', 'padding': '5px','background-color': '#F0F0F0'}, 
             children = [
        html.Div(id = 'left-panel-header', children = [
            html.H1("o l i g o m e r", style={'text-align': 'center', 'margin-bottom': '0'}),
            html.H3("Generator of short PU fragments", style={'text-align': 'center', 'margin-top': '0'}),
            ]),
        html.Div(id = 'left-panel-before-reaction',
            children=[
            html.H2("SELECT SUBSTRATES", style={'font-weight': 'normal', 'margin-top': '50px','margin-bottom': '20px', 'color': 'black',}),
            
            html.Div([
                daq.BooleanSwitch(
                    id='switch-isocyanate',
                    on=False),
                html.H4("Show isocyanates", style={'font-weight': 'normal','margin-top': '0px', 'margin-bottom': '30px', 'margin-left': '10px',
                                                   'color': '#555',
                                'font-size': '14px',
                                'font-weight': '600',
                                'line-height': '25px',
                                'letter-spacing': '.1rem',
                                'text-transform': 'uppercase',
                                'text-decoration': 'none',
                                'font-weight': 'normal',
                                'white-space': 'nowrap'}),
            ],
                style={'display': 'flex', 'align-items': 'left'}),
                    
            html.Div([
                daq.BooleanSwitch(
                    id='switch-hydroxyl',
                    on=False),
                html.H4("Show hydroxyl compounds", style={'font-weight': 'normal','margin-top': '0px', 'margin-bottom': '30px', 'margin-left': '10px',
                                                          'color': '#555',
                                'font-size': '14px',
                                'font-weight': '600',
                                'line-height': '25px',
                                'letter-spacing': '.1rem',
                                'text-transform': 'uppercase',
                                'text-decoration': 'none',
                                'font-weight': 'normal',
                                'white-space': 'nowrap'}),
            ],
                style={'display': 'flex', 'align-items': 'left'}),
            
            html.Div([   
                    
                    dcc.Upload(
                        id='upload-substrates',
                        children=html.Div(['Drag and Drop or ',
                                 html.A('Select File', style={'font-weight': 'bold'})
                                ]),
                        style={
                            'width': '100%',
                            'height': '60px',
                            'lineHeight': '60px',
                            'borderWidth': '1px',
                            'borderStyle': 'dashed',
                            'borderRadius': '5px',
                            'textAlign': 'center',
                            'margin': '0px',
                            'cursor': 'pointer',
                        },               
                        multiple=False
                    ),
                    
                    html.H5(id='successful-upload', children = [], style={'color':'gray', 'margin-top': '5px', 'textAlign': 'center', 'font-weight': 'normal'}), 
                    # html.Div([
                    # html.H4("Upload other substrates", style={'font-weight': 'normal','margin-top': '5px', 'margin-bottom': '0'}),
                    # html.H4("(accepted file format: Name;SMILES)", style={'font-weight': 'normal', 'margin-top': '0'}),
                    # ],
                    # style={'margin-left': '10px',}),  
                
                    dcc.Store(id='uploaded-data'),
                
                ],),
                # style={'display': 'flex', 'align-items': 'left'}),
                 
            
            html.H2("SELECT SIZE", style={'font-weight': 'normal'}),
            dcc.RadioItems(
                    id='select-size',
                    options=[
                        {'label': '2 units', 'value': '2'},
                        {'label': '3 units', 'value': '3'},
                        {'label': '4 units', 'value': '4'},
                    ],
                    value='2',  # Default selected value
                    labelStyle={'display': 'block', 
                                'margin-top': '-5px',
                                'margin-bottom': '10px', 
                                'margin-left': '20px',
                                'color': '#555',
                                'font-size': '15px',
                                'font-weight': '600',
                                'line-height': '25px',
                                'letter-spacing': '.1rem',
                                'text-transform': 'uppercase',
                                'text-decoration': 'none',
                                'font-weight': 'normal',
                                'white-space': 'nowrap'},  # Display the labels on separate lines
                ),
            
            
            html.H2("SELECT CAPPING GROUP", style={'font-weight': 'normal'}),
            dcc.Dropdown(['-NH2', '-CH3', '-N=C=O'], placeholder="Select isocyanate capping", id='capping-group', value='-N=C=O'),
            html.Button("MAKE OLIGOMERS!", id='make-oligomers-button', n_clicks=0, 
                        style={'margin-top': '30px'})

            ]),
    
        html.Div(id = 'left-panel-after-reaction',
            children=[]),
        html.Div(id = 'left-panel-download', style = {'display':'none'},
            children = [
                html.Div([
                html.Button("GENERATE SMILES", id='generate-smiles', n_clicks=0, style={'margin':'5px'} ),
                
                html.Div([
                    dcc.Loading(id='loading-smiles',
                                style ={'margin-left': '15px'},
                                type='dot',
                                children=[html.Div(id="download-smiles", style={'textAlign': 'center', 'margin':'5px','opacity': '0.6'})]
                    )
                ]),
                html.Button("GENERATE 2D STRUCTURES (.mol)", id='generate-mol', n_clicks=0,style={'margin':'5px'}),
                html.Div([
                    dcc.Loading(id='loading-mol',
                                type='dot',
                                children=[html.Div(id="download-mol", style={'textAlign': 'center','margin':'5px','opacity': '0.6'})]
                    )
                ]),
                html.Button("GENERATE 3D STRUCTURES (.mol2)", id='generate-mol2', n_clicks=0,style={'margin':'5px'} ),
                html.Div([
                    dcc.Loading(id='loading-mol2',
                                type='dot',
                                children=[html.Div(id="download-mol2", style={'textAlign': 'center', 'margin':'5px','opacity': '0.6'})]
                    )
                ]),
                html.Button("GENERATE 3D STRUCTURES WITH CONFORMERS (.mol2)", id='generate-conformers', n_clicks=0,style={'margin':'5px'}),
                html.Div([
                    dcc.Loading(id='loading-conformers',
                                type='dot',
                                children=[html.Div(id="download-conformers", style={'textAlign': 'center', 'margin':'5px', 'opacity': '0.6'})]
                    )
                ]),
                html.Button("GENERATE IMAGES (.png)", id='generate-images', n_clicks=0,style={'margin':'5px'} ),
                html.Div([
                    dcc.Loading(id='loading-images',
                                type='dot',
                                children=[html.Div(id="download-images", style={'textAlign': 'center', 'margin':'5px','opacity': '0.6'})]
                    )
                ])
                ], style={'display': 'flex', 'flex-direction': 'column', 'align-items':'flex-start', 'textAlign': 'left'})
            ]),
        dcc.Store(id='store-reaction'),
        html.Div(id = 'left-panel-footer', children = [
            # html.P("Contact", style={'position': 'absolute', 'bottom': '0', 'left': '0', 'right': '0', 'padding': '10px'})
            ]),
    ]),
    html.Div([
        
        html.Div(
            id = 'right-panel-content',
            children = [
                checkbox_list_isocyanate, 
                checkbox_list_hydroxyl,
                
                html.Div(
                    children = [],
                    id = 'reaction-output',
                    style = {'display':'block'}
                )
                ],
            style={})
        ],
        style={'flex': '2'}),
    ])

@app.callback(
    Output('right-panel-content', 'style'),
    Output('hydroxyl-list', 'style'),
    Output('isocyanate-list', 'style'),
    Output('reaction-output', 'children'),
    Output('left-panel-before-reaction', 'style'),
    Output('left-panel-after-reaction', 'children'),
    Output('successful-upload', 'children'),
    Output('left-panel-download', 'style'),
    Output('store-reaction','data'),
    
    Input('switch-isocyanate','on'),
    Input('switch-hydroxyl','on'),
    Input('make-oligomers-button', 'n_clicks'),
    Input('select-size', 'value'),
    Input('isocyanate-list-checkbox', 'value'),
    Input('hydroxyl-list-checkbox', 'value'),
    Input('upload-substrates', 'contents'),
    Input('uploaded-data', 'data'),
    Input('capping-group', 'value') 
)

def make_oligomers(isocyanate_clicks, hydroxyl_clicks, make_oligomer_clicks, size_value, isocyanate_value, hydroxyl_values, contents, file_content, capping_group):

    valid_file = "Accepted input file content: Name;SMILES"
    
    if isocyanate_clicks and hydroxyl_clicks and make_oligomer_clicks == 0 :
        return {'display': 'flex'}, {'flex': '1', 'padding': '10px', 'display':'block'}, {'flex': '1', 'padding': '10px', 'display':'block'}, [], {'display': 'block'}, [], [valid_file], {'display':'none'}, []
    
    elif isocyanate_clicks and make_oligomer_clicks == 0 :
        return {'display': 'flex'}, {'flex': '1', 'padding': '10px', 'display':'none'}, {'flex': '1', 'padding': '10px', 'display':'block'}, [], {'display': 'block'}, [], [valid_file], {'display':'none'}, []
    
    elif hydroxyl_clicks and make_oligomer_clicks == 0 :
        return {'display': 'flex'}, {'flex': '1', 'padding': '10px', 'display':'block'}, {'flex': '1', 'padding': '10px', 'display':'none'}, [], {'display': 'block'}, [], [valid_file], {'display':'none'}, []  
    
     
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
                                valid_smiles = MakeOligomers_dash.is_valid_smiles(comp[1])
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
                        
        return {'display': 'flex'}, {'flex': '1', 'padding': '10px', 'display':'none'}, {'flex': '1', 'padding': '10px', 'display':'none'},[
            html.Img(src='assets/oligomer_main.png', style={'max-width': '100%', 'height': 'auto'})], {'display': 'block'}, [], [valid_file], {'display':'none'}, []  

    elif make_oligomer_clicks:
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
                    valid_smiles = MakeOligomers_dash.is_valid_smiles(comp[1])
                    if not valid_smiles:
                        break
                    else:
                        if comp[1] not in smiles:
                            smiles.append(comp[1])
                        

        if smiles:
            reaction, info, iso_mols, poliol_mols = MakeOligomers_dash.prepare_reaction(smiles)
            
            if reaction:
                reaction_output = "PERFORMED REACTIONS"
                
                if size_value == "2":
                    
                    reagents_smiles, products_smiles = MakeOligomers_dash.perform_dimerization(iso_mols,poliol_mols)
                    
                    capped_products = [MakeOligomers_dash.modify_molecule(product, capping_group[1:]) for product in products_smiles]
                    
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
                                html.Img(src='data:image/jpeg;base64,' + MakeOligomers_dash.smiles_to_image(reagents_smiles[i][0]), 
                                style={'height': '150px','width':'auto', 'margin': '0'}),
                                html.Img(src='assets/plus.png', 
                                style={'height': '10px','width':'auto', 'margin-bottom': '80px'}),
                                html.Img(src='data:image/jpeg;base64,' + MakeOligomers_dash.smiles_to_image(reagents_smiles[i][1]), 
                                style={'height': '150px','width':'auto', 'margin': '0'}),
                                
                                html.Img(src='assets/arrow.png',
                                style={'height': '20px','width':'auto', 'margin-bottom': '75px'}),
                                html.Img(src='data:image/jpeg;base64,' + MakeOligomers_dash.smiles_to_image(product), 
                                style={'height': '150px','width':'auto', 'margin': '0'}),
                                 
                            ])
                            for i,product in enumerate(capped_products)
                        
                        ]
                    )
                    
                elif size_value == "3":
                    
                    reagents_smiles, products_smiles = MakeOligomers_dash.perform_trimerization(iso_mols,poliol_mols)
                    
                    capped_products = [MakeOligomers_dash.modify_molecule(product, capping_group[1:]) for product in products_smiles]
                    
                    reactions = html.Div(
                        [
                            
                            html.Div([
                                
                                html.H4(["Reaction %i: "%(i+1)],style={'font-weight': 'normal', 'margin-left': '20px', 'margin': '0'}),
                                html.Img(src='data:image/jpeg;base64,' + MakeOligomers_dash.smiles_to_image(reagents_smiles[i][0]), 
                                style={'height': '150px','width':'auto', 'margin': '0'}),
                                html.Img(src='assets/plus.png', 
                                style={'height': '10px','width':'auto', 'margin-bottom': '80px'}),
                                html.Img(src='data:image/jpeg;base64,' + MakeOligomers_dash.smiles_to_image(reagents_smiles[i][1]), 
                                style={'height': '150px','width':'auto', 'margin': '0'}),
                                html.Img(src='assets/plus.png', 
                                style={'height': '10px','width':'auto', 'margin-bottom': '80px'}),
                                html.Img(src='data:image/jpeg;base64,' + MakeOligomers_dash.smiles_to_image(reagents_smiles[i][2]), 
                                style={'height': '150px','width':'auto', 'margin': '0'}),
                                
                                html.Img(src='assets/arrow.png',
                                style={'height': '20px','width':'auto', 'margin-bottom': '75px'}),
                                html.Img(src='data:image/jpeg;base64,' + MakeOligomers_dash.smiles_to_image(product), 
                                style={'height': '150px','width':'auto', 'margin': '0'}),
                                 
                            ])
                            for i,product in enumerate(capped_products)
                        
                        ]
                    )
                
                if size_value == "4":
                    
                    reagents_smiles, products_smiles = MakeOligomers_dash.perform_tetramerization(iso_mols,poliol_mols)
                    
                    capped_products = [MakeOligomers_dash.modify_molecule(product, capping_group[1:]) for product in products_smiles]
                    
                    reactions = html.Div(
                        [
                            
                            html.Div([
                                
                                html.H4(["Reaction %i: "%(i+1)],style={'font-weight': 'normal', 'margin-left': '20px', 'margin': '0'}),
                                html.Img(src='data:image/jpeg;base64,' + MakeOligomers_dash.smiles_to_image(reagents_smiles[i][0]), 
                                style={'height': '150px','width':'auto', 'margin': '0'}),
                                html.Img(src='assets/plus.png', 
                                style={'height': '10px','width':'auto', 'margin-bottom': '80px'}),
                                html.Img(src='data:image/jpeg;base64,' + MakeOligomers_dash.smiles_to_image(reagents_smiles[i][1]), 
                                style={'height': '150px','width':'auto', 'margin': '0'}),
                                html.Img(src='assets/plus.png', 
                                style={'height': '10px','width':'auto', 'margin-bottom': '80px'}),
                                html.Img(src='data:image/jpeg;base64,' + MakeOligomers_dash.smiles_to_image(reagents_smiles[i][2]), 
                                style={'height': '150px','width':'auto', 'margin': '0'}),
                                html.Img(src='assets/plus.png', 
                                style={'height': '10px','width':'auto', 'margin-bottom': '80px'}),
                                html.Img(src='data:image/jpeg;base64,' + MakeOligomers_dash.smiles_to_image(reagents_smiles[i][3]), 
                                style={'height': '150px','width':'auto', 'margin': '0'}),
                                
                                html.Img(src='assets/arrow.png',
                                style={'height': '20px','width':'auto', 'margin-bottom': '75px'}),
                                html.Img(src='data:image/jpeg;base64,' + MakeOligomers_dash.smiles_to_image(product), 
                                style={'height': '150px','width':'auto', 'margin': '0'}),
                                 
                            ])
                            for i,product in enumerate(capped_products)
                        
                        ]
                    )
                               
            else:
                reaction_output = """Reactions can't be performed with selected substrates.
                                    Make sure there is at least one hydroxyl compound and one isocyanate."""
                reactions = ""
                products_smiles = ""
            
            
            
        else:
            info = "Select substrates!"

        return {'display': 'flex'}, {'flex': '1', 'padding': '10px', 'display':'none'}, {'flex': '1', 'padding': '10px', 'display':'none'},[
        
        html.Img(src='assets/oligomer_reaction.png', style={'max-width': '100%', 'height': 'auto'}),
        html.Div([html.Div('Number of uploaded substrates: %i'%info[0], style={'margin-bottom':'10px', 'margin-top': '-50px', 'margin-left':'20px'}),
                  html.Div('Substrates types:', style={'margin-left':'20px'}),
                  html.Div('%i isocyanates'%info[1], style={'margin-left':'30px'}),
                  html.Div('%i diisocyanates'%info[2], style={'margin-left':'30px'}),
                  html.Div('%i alcohols/phenols'%info[3], style={'margin-left':'30px'}),
                  html.Div('%i diols'%info[4], style={'margin-left':'30px'}) ], 
                 style = {#'margin-left' : '20px', 'margin-bottom' : '50px', 'color': 'gray', 
                                'color': '#555',
                                'text-align': 'left',
                                'font-size': '16px',
                                'font-weight': '600',
                                'line-height': '25px',
                                'letter-spacing': '.1rem',
                                'text-transform': 'uppercase',
                                'text-decoration': 'none',
                                'font-weight': 'normal',
                                'white-space': 'nowrap'}),
        html.H2([reaction_output], style = {'font-weight': 'normal', 'text-align': 'center',}),# 'margin-left': '20px', 'margin-bottom': '20px', 'margin-top': '10px'}),
        html.Div(reactions)
        
        
        ], {'display': 'none'}, [
            
        html.H2(["%i GENERATED STRUCTURES" %(len(products_smiles))], style = {'font-weight': 'normal', 'margin-top': '100px','margin-bottom':'60px','text-align': 'center',})
            ], [], {'display': 'block'}, products_smiles

@app.callback(
    Output('uploaded-data', 'data'),
    Input('upload-substrates', 'contents')
    
)

def store_uploaded_data(contents):
    if contents is not None:
        # Decode the base64-encoded contents to get the file content
        decoded_contents = base64.b64decode(contents.split(',')[1])
        
        # Convert the bytes content to a string
        file_content = decoded_contents.decode('utf-8')
           
        return file_content
    return None

@app.callback(
    Output('download-smiles', 'children'),
    Input('generate-smiles', 'n_clicks'),
    State('store-reaction', 'data')
)
def generate_smiles(n_clicks, data):
    if n_clicks:
        if data:
            # Generate file content here
            file_content = "\n".join(data)
            
            # Convert the content to bytes
            file_bytes = file_content.encode('utf-8')
            
            # Encode the bytes to base64
            base64_encoded = base64.b64encode(file_bytes).decode('utf-8')
            
            # Create the data URI
            href = f"data:application/octet-stream;charset=utf-8;base64,{base64_encoded}"
            
            return html.A("Download PU_smiles.txt", href=href, download="PU_smiles.txt")
    
    return None

@app.callback(
    Output("download-mol", "children"),
    Input("generate-mol", "n_clicks"),
    State('store-reaction', 'data')
)
def generate_mol(n_clicks, data):
    if n_clicks:
        if data:

        # Create an in-memory buffer to store the zip file content
            zip_buffer = io.BytesIO()

            # Create a zip file in the in-memory buffer
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
                for idx, smiles in enumerate(data):
                    mol_block = MakeOligomers_dash.generate_mol(smiles)
                    mol_filename = f"PU_{idx + 1}.mol"
                    zipf.writestr(mol_filename, mol_block)

            # Rewind the buffer
            zip_buffer.seek(0)
            href = f"data:application/zip;base64,{base64.b64encode(zip_buffer.read()).decode('utf-8')}"
            return html.A("Download PU_2D.zip", href=href, download="PU_2D.zip")
    raise PreventUpdate

@app.callback(
    Output("download-mol2", "children"),
    Input("generate-mol2", "n_clicks"),
    State('store-reaction', 'data')
)
def generate_mol2(n_clicks, data):
    if n_clicks:
        if data:

        # Create an in-memory buffer to store the zip file content
            zip_buffer = io.BytesIO()

            # Create a zip file in the in-memory buffer
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
                for idx, smiles in enumerate(data):
                    mol_block = MakeOligomers_dash.generate_mol2(smiles, idx)
                    mol_filename = f"PU_{idx + 1}.mol2"
                    zipf.writestr(mol_filename, mol_block)

            # Rewind the buffer
            zip_buffer.seek(0)
            href = f"data:application/zip;base64,{base64.b64encode(zip_buffer.read()).decode('utf-8')}"
            return html.A("Download PU_3D.zip", href=href, download="PU_3D.zip")
    raise PreventUpdate

@app.callback(
    Output("download-conformers", "children"),
    Input("generate-conformers", "n_clicks"),
    State('store-reaction', 'data')
)
def generate_conformers(n_clicks, data):
    if n_clicks:
        if data:

        # Create an in-memory buffer to store the zip file content
            zip_buffer = io.BytesIO()

            # Create a zip file in the in-memory buffer
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
                for idx, smiles in enumerate(data):
                    conformers_content = MakeOligomers_dash.generate_conformers(smiles, idx)
                    for conf_num, conformer in enumerate(conformers_content):
                        mol_filename = f"PU_{idx + 1}_{conf_num}.mol2"
                        zipf.writestr(mol_filename, conformer)

            # Rewind the buffer
            zip_buffer.seek(0)
            href = f"data:application/zip;base64,{base64.b64encode(zip_buffer.read()).decode('utf-8')}"
            return html.A("Download PU_3D_conformers.zip", href=href, download="PU_3D_conformers.zip")
    raise PreventUpdate

@app.callback(
    Output("download-images", "children"),
    Input("generate-images", "n_clicks"),
    State('store-reaction', 'data')
)
def generate_images(n_clicks, data):
    if n_clicks:
        if data:

        # Create an in-memory buffer to store the zip file content
            zip_buffer = io.BytesIO()

            # Create a zip file in the in-memory buffer
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
                for idx, smiles in enumerate(data):
                    mol_block = MakeOligomers_dash.generate_image(smiles)
                    mol_filename = f"PU_{idx + 1}.png"
                    zipf.writestr(mol_filename, mol_block)

            # Rewind the buffer
            zip_buffer.seek(0)
            href = f"data:application/zip;base64,{base64.b64encode(zip_buffer.read()).decode('utf-8')}"
            return html.A("Download PU_images.zip", href=href, download="PU_images.zip")
    raise PreventUpdate
# Run the app
if __name__ == '__main__':
    app.run_server(debug=False)
