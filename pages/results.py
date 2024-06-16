import dash
from dash import html, dcc, callback, dash_table
from dash.dependencies import Input, Output, State
import callbacks
import utils
import pandas as pd
import io
import zipfile
import tempfile


dash.register_page(__name__, 
                   path='/results',
                   title='results PUR-GEN',
                   name='results PUR-GEN',
                   image='assets/logo.png')

layout = html.Div(id = 'resluts-page', style = {'display': 'block'},
                      
    children = [
        html.Center(style = {'alignItems': 'center', 'background-color': '#F0F0F0'},
        children = [html.A(html.Img(src='assets/pur-gen.png', className = 'homepage-logo'),href='/'),]),
        
        html.Div(style={'display':'flex'}, children=[
        html.Div(style={'flex':'1'},children=[
            html.H3('INPUT STRUCTURES AND PARAMETERS', className='highlighted-left-text-margin'),
            html.Div(id = 'summary-output')]),

        html.Div(style={'flex':'1'},children=[
            html.H3('DOWNLOAD RESULTS', className='highlighted-left-text-margin'),
            html.Div(className = 'results-buttons', children=[
            
            # Download button - 2D structures (zipped .mol files)
             html.Div(style={'margin-bottom': '10px'}, children=[
                 dcc.Loading(
                    id='loading-2d',
                    type='circle',  # You can use 'default', 'circle', or 'dot'
                    children=[
                 html.Button('2D STRUCTURES (.mol)', id='generate-2d', n_clicks=0),
                 dcc.Download(id="download-2d")])]),

            # Download button - 3D structures (zipped .mol2 files)
             html.Div(style={'margin-bottom': '10px'}, children=[
                 dcc.Loading(
                    id='loading-3d',
                    type='circle',  # You can use 'default', 'circle', or 'dot'
                    children=[
                 html.Button('3D STRUCTURES (.mol2)', id='generate-3d', n_clicks=0),
                 dcc.Download(id='download-3d')])]),

            # Download button - 3D structures with conformers (zipped .mol2 files)
             html.Div(style={'margin-bottom': '10px'}, children=[
                 dcc.Loading(
                    id='loading-conformers',
                    type='circle',  # You can use 'default', 'circle', or 'dot'
                    children=[
                        html.Button('3D CONFORMERS (.mol2)', id='generate-conformers', n_clicks=0),
                        dcc.Download(id='download-conformers')])]),
             html.H4("Generation of conformers may take longer, especially with numerous compounds.",
                                className='run-select-info-text'), 
            
            # Download button - properties table (.csv file)
             html.Div(style={'margin-bottom': '10px'}, children=[
                 dcc.Loading(
                    id='loading-csv',
                    type='circle',  # You can use 'default', 'circle', or 'dot'
                    children=[
                 html.Button('PROPERTIES (.csv)', id='generate-csv', n_clicks=0),
                 dcc.Download(id="download-csv")])])
                ]),
            ]),

        dcc.Store(id='products')]),

        html.H1('GENERATED PUR FRAGMENTS',className='highlighted-center-text'),
        dcc.Tabs(id="tabs", value='tab-structures', children=[
            dcc.Tab(label='PUR structres', value='tab-structures'),
            dcc.Tab(label='Calculated properties', value='tab-table'),
            dcc.Tab(label='Properties histograms', value='tab-histograms'),
            ]),
        html.Div(id = 'tabs-output')      
        ])


# Access stored substrates, size and capping and perform reaction
@callback(
        Output('summary-output', 'children'),
        Output('tabs-output', 'children'),
        Output('products', 'data'),
        Input('stored-substrates', 'data'),
        Input('stored-size', 'data'),
        Input('stored-capping', 'data'),
        Input('tabs', 'value')
        )
def process_substrates(stored_substrates, stored_size, stored_capping, tab): 

    summary, structures_imgs, capped_products = callbacks.show_reactions(stored_substrates, stored_size, stored_capping)

    products_df = pd.DataFrame({'Compound':pd.Index(range(1, len(capped_products) + 1)),'SMILES':capped_products})
    compounds_properties_df = utils.calculate_properties_df(products_df)
    table = dash_table.DataTable(compounds_properties_df.to_dict('records'),
                                 style_data={'textAlign': 'left'},
                                 style_header={'textAlign': 'left'})
    fig = utils.generate_properties_figure(compounds_properties_df)

    if tab == 'tab-structures':
        tab_output = structures_imgs
    elif tab == 'tab-table':
        tab_output = html.Div(children=[
            html.Center(html.H4('''Calculated PUR fragments properties:
                    molecular weight, heavy atom count, number of rotatable bonds, 
            presence of ester and ether bonds, count of aromatic atoms, aromatic proportion 
            (ratio of aromatic atoms to heavy atoms), Crippen-Wildman partition coefficient 
            (cLogP), topological polar surface area 
            (TPSA) and Crippen-Wildman molar refraction (MR).''', 
                    className = 'results-properties-description')),
            table,
            html.Br()])
    elif tab == 'tab-histograms':
        tab_output = html.Div(children=[
            html.Center(html.H4('''Calculated PUR fragments properties:
                    molecular weight, heavy atom count, number of rotatable bonds, 
            presence of ester and ether bonds, count of aromatic atoms, aromatic proportion 
            (ratio of aromatic atoms to heavy atoms), Crippen-Wildman partition coefficient 
            (cLogP), topological polar surface area 
            (TPSA) and Crippen-Wildman molar refraction (MR).''', 
                    className = 'results-properties-description')),
            dcc.Graph(figure=fig)])
    return summary, tab_output, compounds_properties_df.to_dict()

#Download csv
@callback(
    Output('download-csv', 'data'),
    Input('generate-csv', 'n_clicks'),
    State('products', 'data'),
    prevent_initial_call=True
)
def download_csv(n_clicks, data):
    if n_clicks:
        df=pd.DataFrame(data)
    return dcc.send_data_frame(df.to_csv, "properties.csv")

#Download 2d
@callback(
    Output('download-2d', 'data'),
    Input('generate-2d', 'n_clicks'),
    State('products', 'data'),
    prevent_initial_call=True
)
def download_mol(n_clicks, data):
    if n_clicks:
        df = pd.DataFrame(data)
        smiles_list = df['SMILES'].values
        zip_buffer = io.BytesIO()
        # Create a zip file in the in-memory buffer
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
            for idx, smiles in enumerate(smiles_list):
                mol_block = utils.generate_mol(smiles)
                mol_filename = f"PUR_{idx + 1}.mol"
                zipf.writestr(mol_filename, mol_block)
        zip_buffer.seek(0) 
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=True) as tmp_file:
            tmp_file.write(zip_buffer.getvalue())
            tmp_file_name = tmp_file.name
            return dcc.send_file(tmp_file_name, filename="PUR_2D.zip")
        
#Download 3d
@callback(
    Output('download-3d', 'data'),
    Input('generate-3d', 'n_clicks'),
    State('products', 'data'),
    prevent_initial_call=True
)
def download_mol2(n_clicks, data):
    if n_clicks:
        df = pd.DataFrame(data)
        smiles_list = df['SMILES'].values
        zip_buffer = io.BytesIO()
        # Create a zip file in the in-memory buffer
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
            for idx, smiles in enumerate(smiles_list):
                mol_block = utils.generate_mol2(smiles, idx)
                mol_filename = f"PUR_{idx + 1}.mol2"
                zipf.writestr(mol_filename, mol_block)
        # Rewind the buffer
        zip_buffer.seek(0)      
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=True) as tmp_file:
            tmp_file.write(zip_buffer.getvalue())
            tmp_file_name = tmp_file.name
            return dcc.send_file(tmp_file_name, filename="PUR_3D.zip")
        
#Download conformers
@callback(
    Output('download-conformers', 'data'),
    Input('generate-conformers', 'n_clicks'),
    State('products', 'data'),
    prevent_initial_call=True
)
def download_conformers(n_clicks, data):
    if n_clicks:
        df = pd.DataFrame(data)
        smiles_list = df['SMILES'].values
        zip_buffer = io.BytesIO()
        # Create an in-memory buffer to store the zip file content
        zip_buffer = io.BytesIO()

        # Create a zip file in the in-memory buffer
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
            for idx, smiles in enumerate(smiles_list):
                conformers_content = utils.generate_conformers(smiles, idx)
                for conf_num, conformer in enumerate(conformers_content):
                    mol_filename = f"PUR_{idx + 1}_{conf_num}.mol2"
                    zipf.writestr(mol_filename, conformer)

        # Rewind the buffer
        zip_buffer.seek(0)   
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=True) as tmp_file:
            tmp_file.write(zip_buffer.getvalue())
            tmp_file_name = tmp_file.name
            return dcc.send_file(tmp_file_name, filename="PUR_3D_conformers.zip")



