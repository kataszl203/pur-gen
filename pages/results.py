# import dash
# from dash import html, dcc, callback, dash_table
# from dash.dependencies import Input, Output, State
# import layouts
# import callbacks
# import utils
# import pandas as pd
# from plotly.subplots import make_subplots
# import plotly.graph_objects as go
# import io
# from dash.exceptions import PreventUpdate
# import zipfile
# import tempfile
# import base64
# import os

# dash.register_page(__name__, path='/results')

# external_stylesheets = ['assets/style.css']

# layout = html.Div(id = 'resluts-page', style = {'display': 'block'},
#     children = [
#         html.Center(style = {'alignItems': 'center', 'height': 'auto', 'background-color': '#F0F0F0'},
#         children = [html.A(html.Img(src='assets/pur-gen.png', className = 'homepage-logo'),href='/'),
#                     ]),
#         html.Div(children=[
#         html.Div(style={'flex':'1'},children=[
#         html.H3('INPUT STRUCTURES AND PARAMETERS', className='highlighted-left-text'),
#         html.Div(id = 'summary-output')]),
#         html.Div(style={'flex':'1'},
#             children=[
#             html.H3('DOWNLOAD RESULTS', className='highlighted-left-text'),
#             html.Div(style={'display':'block', 'justify-content': 'center', 'margin-top':'50px', 'margin-bottom':'30px'},
#                          children=[
#              html.Div(style={'margin-bottom': '10px'}, children=[
#                  html.Button('2D STRUCTURES (.mol)', id='generate-2d', n_clicks=0),
#                  html.Div(id='download-2d')]),
#              html.Div(style={'margin-bottom': '10px'}, children=[
#                  html.Button('3D STRUCTURES (.mol2)', id='generate-3d', n_clicks=0),
#                  html.Div(id='download-3d')]),
#              html.Div(style={'margin-bottom': '10px'}, children=[
#                  html.Button('3D CONFORMERS (.mol2)', id='generate-conformers', n_clicks=0),
#                  html.Div(id='download-conformers')]),
            

#              html.Div(style={'margin-bottom': '10px'}, children=[
#                  html.A(html.Button('PROPERTIES (.csv)', id='generate-csv', n_clicks=0), id='download-link', href='', download='products.csv'),
#                  html.Div(id="download-csv")])
#             #RAMEZ
#             <button type="submit" id="downloadDataBtn" formaction="{{ url_for('download_excel') }}">Download Data</button>
#          ]),
#             ]
#         ),
#         dcc.Store(id='products'),
        
#         ],style={'display':'flex'}

#         ),
#         html.H1('GENERATED PUR FRAGMENTS',className='highlighted-center-text'),
#         dcc.Tabs(id="tabs", value='tab-structures', children=[
#         dcc.Tab(label='PUR structres', value='tab-structures'),
#         dcc.Tab(label='Calculated properties', value='tab-table'),
#         dcc.Tab(label='Properties histograms', value='tab-histograms'),
#         ]),
#         html.Div(id = 'tabs-output')      
#                 ])



# # Access stored substrates, size and capping and perform reaction
# @callback(
#         Output('summary-output', 'children'),
#         Output('tabs-output', 'children'),
#         Output('products', 'data'),
#         Input('stored-substrates', 'data'),
#         Input('stored-size', 'data'),
#         Input('stored-capping', 'data'),
#         Input('tabs', 'value')
#         )
# def process_substrates(stored_substrates, stored_size, stored_capping, tab): 
#     summary, structures_imgs, capped_products = callbacks.show_reactions(stored_substrates, stored_size, stored_capping)

#     products_df = pd.DataFrame({'Compound':pd.Index(range(1, len(capped_products) + 1)),'SMILES':capped_products})
#     compounds_properties_df = utils.calculate_properties_df(products_df)
#     table = dash_table.DataTable(compounds_properties_df.to_dict('records'))

#     properties=['Molecular Weight', 'Heavy Atoms', 'Rotable Bonds', 'Ester bond', 'Ether bond',
#                 'Aromatic Atoms', 'Aromatic Proportion', 'clogP', 'TPSA', 'MR']
#     fig = make_subplots(rows=2, cols=5, subplot_titles=properties)
#     row_i = 1
#     col_i = 1
#     for i in range(len(properties)):
#         if col_i == 6:
#             row_i += 1
#             col_i = 1
#         fig.add_trace(
#             go.Histogram(x=compounds_properties_df[properties[i]]),
#             row=row_i, col=col_i
#         )
#         col_i += 1
#     fig.update_layout(showlegend=False)

#     if tab == 'tab-structures':
#         tab_output = structures_imgs
#     elif tab == 'tab-table':
#         tab_output = table
#     elif tab == 'tab-histograms':
#         tab_output = dcc.Graph(figure=fig)
#     return summary, tab_output, compounds_properties_df.to_dict()

# @callback(
#         Output('download-link','href'),
#         Input('products', 'data'),
#         Input('generate-csv','n_clicks'),
#         )

# def generate_download_link(products, n_clicks_csv):
#     if products:
#         if n_clicks_csv:
#             products_df = pd.DataFrame(products)
#             csv_string = products_df.to_csv(index=False, encoding='utf-8')
#             flask.session["csv_data"] = csv_string  # Store the CSV data in Flask session
#             return '/download-csv'


# # Generate data to download
# # @callback(
# #         Output('download-2d','children'),
# #         Output('download-3d','children'),
# #         Output('download-conformers','children'),
# #         Output('download-csv','data'),

# #         Input('products', 'data'),
# #         Input('generate-2d','n_clicks'),
# #         Input('generate-3d','n_clicks'),
# #         Input('generate-conformers','n_clicks'),
# #         Input('generate-csv','n_clicks'),

# #         prevent_initial_call=True,
# #         )

# # def generate_download(products, n_clicks_2d, n_clicks_3d, 
# #                       n_clicks_conformers, n_clicks_csv):
    
# #     download_2d = []
# #     download_3d = []
# #     download_conformers = []
# #     download_csv = []

# #     products_df = pd.DataFrame(products)
# #     products_list = products_df['SMILES'].values

# #     if n_clicks_2d:
# #         if products:
# #             with tempfile.TemporaryDirectory() as temp_dir:
# #                 zip_path = os.path.join(temp_dir, "PUR_2D.zip")
# #                 with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
# #                     for idx, smiles in enumerate(products_list):
# #                         mol_block = utils.generate_mol(smiles)
# #                         mol_filename = f"PUR_{idx + 1}.mol"
# #                         zipf.writestr(mol_filename, mol_block)
# #             download_2d = html.Div([
# #     html.A("Download PUR_2D.zip", href="/download", download="PUR_2D.zip"),
# # ])

# #             # # Create an in-memory buffer to store the zip file content
# #             # zip_buffer = io.BytesIO()

# #             # # Create a zip file in the in-memory buffer
# #             # with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
# #             #     for idx, smiles in enumerate(products_list):
# #             #         mol_block = utils.generate_mol(smiles)
# #             #         mol_filename = f"PUR_{idx + 1}.mol"
# #             #         zipf.writestr(mol_filename, mol_block)

# #             # # Rewind the buffer
# #             # zip_buffer.seek(0)

# #             # # Encode the zip file content to base64
# #             # zip_content_base64 = base64.b64encode(zip_buffer.read()).decode('utf-8')

# #             # # Create the download link
# #             # href = f"data:application/zip;base64,{zip_content_base64}"
# #             # download_2d = html.A("Download PUR_2D.zip", href=href, download="PUR_2D.zip", target="_blank")
    
# #     if n_clicks_csv:
# #         download_csv = dcc.send_data_frame(products_df.to_csv, "PUR_properties.csv")


# #     return download_2d, download_3d, download_conformers, download_csv

