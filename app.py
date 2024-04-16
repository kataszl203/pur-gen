import dash
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import utils
import io
import base64
import zipfile
import layouts
import callbacks
import flask
import os
import pandas as pd
from datetime import datetime
import urllib.parse


# server = app.server
server = flask.Flask(__name__)
app = dash.Dash(__name__, use_pages=True, server = server, external_stylesheets = ['assets/style.css'])
app.secret_key = "1d96c89adac1d05d77ef40707758213f"
server.config["SECRET_KEY"]="1d96c89adac1d05d77ef40707758213f"

products = None

## INSERTED PAGE
dash.register_page(__name__, path='/results',
    
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
                 html.Button('2D STRUCTURES (.mol)', id='generate-2d', n_clicks=0),
                 html.Div(id='download-2d')]),

            # Download button - 3D structures (zipped .mol2 files)
             html.Div(style={'margin-bottom': '10px'}, children=[
                 html.Button('3D STRUCTURES (.mol2)', id='generate-3d', n_clicks=0),
                 html.Div(id='download-3d')]),

            # Download button - 3D structures with conformers (zipped .mol2 files)
             html.Div(style={'margin-bottom': '10px'}, children=[
                 html.Button('3D CONFORMERS (.mol2)', id='generate-conformers', n_clicks=0),
                 html.Div(id='download-conformers')]),
            
            # Download button - properties table (.csv file)
             html.Div(style={'margin-bottom': '10px'}, children=[
                 html.A(html.Button('PROPERTIES (.csv)', id='generate-csv', n_clicks=0), 
                        id='download-csv', href='/download-csv', download='products.csv')
                        # html.Button('PROPERTIES (.csv)', id='generate-csv', n_clicks=0),
                        # dcc.Download(id="download-csv"),
                # html.A(html.Button('PROPERTIES (.csv)', id='generate-csv', n_clicks=0), 
                #         id='download-link', href=f'data:text/csv;charset=utf-8,{products}', download='products.csv'),
                #  html.A('csv_link',id='download-link', href='/download-csv',download='products.csv'),
                    ])
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
    )

# Access stored substrates, size and capping and perform reaction
@app.callback(
        Output('summary-output', 'children'),
        Output('tabs-output', 'children'),
        Output('products', 'data'),
        Input('stored-substrates', 'data'),
        Input('stored-size', 'data'),
        Input('stored-capping', 'data'),
        Input('tabs', 'value')
        )
def process_substrates(stored_substrates, stored_size, stored_capping, tab): 

    global products

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
                    molecular weight, number of heavy atoms, 
                    number of rotatable bonds, presence of ester bond, 
                    presence of ether bond, number of aromatic atoms, 
                    aromatic proportion (number of aromatic atoms divided
                     by number of heavy atoms), Crippen-Wildman partition 
                    coefficient (clogP), topological polar surface area (TPSA), 
                    Crippen-Wildman molar refractivity (MR).''', 
                    className = 'results-properties-description')),
            table])
    elif tab == 'tab-histograms':
        tab_output = html.Div(children=[
            html.Center(html.H4('''Calculated PUR fragments properties:
                    molecular weight, number of heavy atoms, 
                    number of rotatable bonds, presence of ester bond, 
                    presence of ether bond, number of aromatic atoms, 
                    aromatic proportion (number of aromatic atoms divided
                     by number of heavy atoms), Crippen-Wildman partition 
                    coefficient (clogP), topological polar surface area (TPSA), 
                    Crippen-Wildman molar refractivity (MR).''', 
                    className = 'results-properties-description')),
            dcc.Graph(figure=fig)])

    products = compounds_properties_df
    return summary, tab_output, compounds_properties_df.to_dict()

# @app.callback(
#         Output('download-csv',"data"),
#         Input('products', 'data'),
#         Input('generate-csv','n_clicks'),
#         )

# def generate_download_link(products, n_clicks_csv):
#     if products:
#         if n_clicks_csv:
#             products_df = pd.DataFrame(products)
#             csv_string = products_df.to_csv(index=False, encoding='utf-8')
#             flask.session["csv_data"] = csv_string  # Store the CSV data in Flask session
#             # return 
## INSERTED PAGE

# def generate_csv(data,n_clicks):
#     if n_clicks == 0:
#         raise PreventUpdate
#     df=pd.DataFrame(data)
#     csv_string = df.to_csv(index=False, encoding='utf-8')
#     csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
#     return dict(content=csv_string, filename="products.csv")

app.layout = html.Div([
    dcc.Store(id='stored-substrates', data=[]),
    dcc.Store(id='stored-size'),
    dcc.Store(id='stored-capping'),
    dash.page_container
])

@app.server.route("/download-csv", methods=["POST"])
def download_csv():
    if products is not None:
        csv_data = io.StringIO()
        products.to_csv(csv_data, index=False, encoding='utf-8')
        csv_data.seek(0)
        response = flask.make_response(csv_data.getvalue())

        current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"sdr_{current_datetime}.csv"

        response.headers["Content-Disposition"] = f"attachment; filename={filename}"

        response.headers["Content-Type"] = "text/csv"  # Change content type to text/csv

        return response
    else:
        return "No data available", 404


    # response = flask.Flask.make_response(data.getvalue())

    # return response
    # return flask.Response(
    #     data,
    #     mimetype="text/csv",
    #     headers={"Content-disposition": "attachment; filename=products.csv"}
    # )

# @app.route('/download_csv', methods=['POST'])
# @login_required
# def download_csv():
#     if result is not None:
#         # Convert the result DataFrame to CSV format
#         csv_data = StringIO()
#         result.to_csv(csv_data, index=False)
#         csv_data.seek(0)  # Move to the beginning after writing

#         current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#         filename = f"sdr_{current_datetime}.csv"

#         # Create a response with the CSV data
#         response = make_response(csv_data.getvalue())  # Use getvalue() to get the string from StringIO
#         response.headers["Content-Disposition"] = f"attachment; filename={filename}"
#         response.headers["Content-Type"] = "text/csv"  # Change content type to text/csv

#         return response
#     else:
#         return "No data available", 404


#RAMEZ CODE
# @app.route('/download_excel', methods=['POST'])
# @login_required
# def download_excel():

#     if result is not None:
#         # Convert the result DataFrame to Excel format
#         excel_data = BytesIO()
#         result.to_excel(excel_data, index=False)
#         excel_data.seek(0)

#         current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#         filename = f"sdr_{current_datetime}.xlsx"

#         # Create a response with the Excel data
#         response = make_response(excel_data.read())
#         response.headers["Content-Disposition"] = f"attachment; filename={filename}"
#         response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

#         return response
#     else:
#         return "No data available", 404


# @app.callback(
#     Output('right-panel-content', 'style'),
#     Output('main-page', 'style'),
#     Output('hydroxyl-list', 'style'),
#     Output('isocyanate-list', 'style'),
#     Output('right-panel-header', 'style'),
#     Output('main-after-reaction', 'style'),
#     Output('reaction-output', 'children'),
#     Output('left-panel-before-reaction', 'style'),
#     Output('left-panel-after-reaction', 'children'),
#     Output('successful-upload', 'children'),
#     Output('left-panel-download', 'style'),
#     Output('store-reaction','data'),

#     Input('switch-isocyanate','on'),
#     Input('switch-hydroxyl','on'),
#     Input('make-oligomers-button', 'n_clicks'),
#     Input('select-size', 'value'),
#     Input('select-all-isocyanate', 'value'),
#     Input('select-all-hydroxyl', 'value'),
#     Input('isocyanate-list-checkbox', 'value'),
#     Input('hydroxyl-list-checkbox', 'value'),
#     Input('upload-substrates', 'contents'),
#     Input('uploaded-data', 'data'),
#     Input('capping-group', 'value') 
# )

# def make_oligomers(isocyanate_clicks, hydroxyl_clicks, make_oligomer_clicks, size_value, all_isocyanate, all_hydroxyl, isocyanate_value, hydroxyl_values, contents, file_content, capping_group):
#     right_panel_content_style, main_page_style, hydroxyl_list_style, isocyanate_list_style, right_panel_header_style, main_after_reaction_style, reaction_output_children, left_panel_before_style, left_panel_after_children, successful_upload_children, left_panel_download_style, store_reaction_data = callbacks.handle_display_styles(isocyanate_clicks, hydroxyl_clicks, make_oligomer_clicks, size_value, all_isocyanate, all_hydroxyl, isocyanate_value, hydroxyl_values, contents, file_content, capping_group, isocyanate_all, hydroxyl_all)
    
#     return right_panel_content_style, main_page_style, hydroxyl_list_style, isocyanate_list_style, right_panel_header_style, main_after_reaction_style, reaction_output_children, left_panel_before_style, left_panel_after_children, successful_upload_children, left_panel_download_style, store_reaction_data


# @app.callback(
#     Output('uploaded-data', 'data'),
#     Input('upload-substrates', 'contents')
# )

# def store_uploaded_data(contents):
#     if contents is not None:
#         # Decode the base64-encoded contents to get the file content
#         decoded_contents = base64.b64decode(contents.split(',')[1])
        
#         # Convert the bytes content to a string
#         file_content = decoded_contents.decode('utf-8')
           
#         return file_content
#     return None

# @app.callback(
#     Output('download-smiles', 'children'),
#     Input('generate-smiles', 'n_clicks'),
#     State('store-reaction', 'data')
# )
# def generate_smiles(n_clicks, data):
#     if n_clicks:
#         if data:
#             # Generate file content here
#             file_content = "\n".join(data)
            
#             # Convert the content to bytes
#             file_bytes = file_content.encode('utf-8')
            
#             # Encode the bytes to base64
#             base64_encoded = base64.b64encode(file_bytes).decode('utf-8')
            
#             # Create the data URI
#             href = f"data:application/octet-stream;charset=utf-8;base64,{base64_encoded}"
            
#             return html.A("Download PUR_smiles.txt", href=href, download="PUR_smiles.txt")
    
#     return None

# @app.callback(
#     Output("download-mol", "children"),
#     Input("generate-mol", "n_clicks"),
#     State('store-reaction', 'data')
# )
# def generate_mol(n_clicks, data):
#     if n_clicks:
#         if data:

#         # Create an in-memory buffer to store the zip file content
#             zip_buffer = io.BytesIO()

#             # Create a zip file in the in-memory buffer
#             with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
#                 for idx, smiles in enumerate(data):
#                     mol_block = utils.generate_mol(smiles)
#                     mol_filename = f"PUR_{idx + 1}.mol"
#                     zipf.writestr(mol_filename, mol_block)

#             # Rewind the buffer
#             zip_buffer.seek(0)
#             href = f"data:application/zip;base64,{base64.b64encode(zip_buffer.read()).decode('utf-8')}"
#             return html.A("Download PUR_2D.zip", href=href, download="PUR_2D.zip")
#     raise PreventUpdate

# @app.callback(
#     Output("download-mol2", "children"),
#     Input("generate-mol2", "n_clicks"),
#     State('store-reaction', 'data')
# )
# def generate_mol2(n_clicks, data):
#     if n_clicks:
#         if data:

#         # Create an in-memory buffer to store the zip file content
#             zip_buffer = io.BytesIO()

#             # Create a zip file in the in-memory buffer
#             with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
#                 for idx, smiles in enumerate(data):
#                     mol_block = utils.generate_mol2(smiles, idx)
#                     mol_filename = f"PUR_{idx + 1}.mol2"
#                     zipf.writestr(mol_filename, mol_block)

#             # Rewind the buffer
#             zip_buffer.seek(0)
#             href = f"data:application/zip;base64,{base64.b64encode(zip_buffer.read()).decode('utf-8')}"
#             return html.A("Download PUR_3D.zip", href=href, download="PUR_3D.zip")
#     raise PreventUpdate

# @app.callback(
#     Output("download-conformers", "children"),
#     Input("generate-conformers", "n_clicks"),
#     State('store-reaction', 'data')
# )
# def generate_conformers(n_clicks, data):
#     if n_clicks:
#         if data:

#         # Create an in-memory buffer to store the zip file content
#             zip_buffer = io.BytesIO()

#             # Create a zip file in the in-memory buffer
#             with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
#                 for idx, smiles in enumerate(data):
#                     conformers_content = utils.generate_conformers(smiles, idx)
#                     for conf_num, conformer in enumerate(conformers_content):
#                         mol_filename = f"PUR_{idx + 1}_{conf_num}.mol2"
#                         zipf.writestr(mol_filename, conformer)

#             # Rewind the buffer
#             zip_buffer.seek(0)
#             href = f"data:application/zip;base64,{base64.b64encode(zip_buffer.read()).decode('utf-8')}"
#             return html.A("Download PUR_3D_conformers.zip", href=href, download="PUR_3D_conformers.zip")
#     raise PreventUpdate

# @app.callback(
#     Output("download-images", "children"),
#     Input("generate-images", "n_clicks"),
#     State('store-reaction', 'data')
# )
# def generate_images(n_clicks, data):
#     if n_clicks:
#         if data:

#         # Create an in-memory buffer to store the zip file content
#             zip_buffer = io.BytesIO()

#             # Create a zip file in the in-memory buffer
#             with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
#                 for idx, smiles in enumerate(data):
#                     mol_block = utils.generate_image(smiles)
#                     mol_filename = f"PUR_{idx + 1}.png"
#                     zipf.writestr(mol_filename, mol_block)

#             # Rewind the buffer
#             zip_buffer.seek(0)
#             href = f"data:application/zip;base64,{base64.b64encode(zip_buffer.read()).decode('utf-8')}"
#             return html.A("Download PUR_images.zip", href=href, download="PUR_images.zip")
#     raise PreventUpdate

# Run the app
if __name__ == '__main__':
    app.run_server(debug=False)
