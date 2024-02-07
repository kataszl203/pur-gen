import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import utils
import io
import base64
import zipfile
import layouts
import callbacks

# Create the Dash app
app = dash.Dash(__name__)
server = app.server

external_stylesheets = ['assets/style.css']

# Read the compounds
isocyanate_list = [{'label' : i.split(";")[0], 'smiles' : i.split(";")[1]} for i in open("data/isocyanates.txt", "r").read().splitlines()]
hydroxyl_list = [{'label' : i.split(";")[0], 'smiles' : i.split(";")[1]} for i in open("data/poliols.txt", "r").read().splitlines()]
isocyanate_all = [item['smiles'] for item in isocyanate_list]
hydroxyl_all = [item['smiles'] for item in hydroxyl_list]

# Define the layout of the app
app.layout = html.Div(
    style={'display': 'flex'},
    children=[html.Div(id = 'left-panel-content',
                       style = {'flex': '1', 
                                'padding': '5px',
                                'background-color': '#F0F0F0'},
                       children = [html.Div(id = 'left-panel-header',
                                            children = [html.A(html.Img(src='assets/pur-gen.png', 
                                                                 style={'max-width': '85%', 
                                                                        'height': 'auto'}), href='/'),
                                                        ]),
                                   html.Div(id = 'left-panel-before-reaction',
                                            children = [html.H3("SELECT SUBSTRATES",
                                                                style={'font-weight': 'normal',
                                                                       'margin-top': '20px',
                                                                       'margin-bottom': '0px',
                                                                       'color': 'black',}),
                                                        html.H5("Choose at least one isocyanate and one hydroxyl compound.",
                                                                style={'font-weight': 'normal',
                                                                       'color': 'gray',
                                                                       'margin-top': '5px',
                                                                       'margin-bottom': '15px'}),
                                                        layouts.create_switch_with_label('show isocyanates','switch-isocyanate'),
                                                        layouts.create_switch_with_label('show hydroxyl compounds','switch-hydroxyl'),
                                                        layouts.create_upload_component(),
                                                        layouts.create_select_size_component(),
                                                        layouts.create_capping_group_component()
                                                        ]),
                                   html.Div(id = 'left-panel-after-reaction',
                                            children=[]),
                                   layouts.create_download_panel(),
                                   dcc.Store(id='store-reaction'),
                                   layouts.create_footer()
                                   ]),
              html.Div([
                  html.Div(id = 'right-panel-content',
                           children = [layouts.create_checkbox_list(isocyanate_list, "Select isocyanates: ", 'isocyanate-list', 'select-all-isocyanate', 'isocyanate-list-checkbox'),
                                       layouts.create_checkbox_list(hydroxyl_list, "Select hydroxyl compounds:", 'hydroxyl-list', 'select-all-hydroxyl', 'hydroxyl-list-checkbox'),
                                       layouts.create_right_panel(),
                                       html.Div(id = 'reaction-output',
                                                children = [],
                                                style = {'display':'block'}
                                                )],
                           style={})],
                       style={'flex': '2'}),
              ])

@app.callback(
    Output('right-panel-content', 'style'),
    Output('main-page', 'style'),
    Output('hydroxyl-list', 'style'),
    Output('isocyanate-list', 'style'),
    Output('right-panel-header', 'style'),
    Output('main-after-reaction', 'style'),
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
    Input('select-all-isocyanate', 'value'),
    Input('select-all-hydroxyl', 'value'),
    Input('isocyanate-list-checkbox', 'value'),
    Input('hydroxyl-list-checkbox', 'value'),
    Input('upload-substrates', 'contents'),
    Input('uploaded-data', 'data'),
    Input('capping-group', 'value') 
)

def make_oligomers(isocyanate_clicks, hydroxyl_clicks, make_oligomer_clicks, size_value, all_isocyanate, all_hydroxyl, isocyanate_value, hydroxyl_values, contents, file_content, capping_group):
    right_panel_content_style, main_page_style, hydroxyl_list_style, isocyanate_list_style, right_panel_header_style, main_after_reaction_style, reaction_output_children, left_panel_before_style, left_panel_after_children, successful_upload_children, left_panel_download_style, store_reaction_data = callbacks.handle_display_styles(isocyanate_clicks, hydroxyl_clicks, make_oligomer_clicks, size_value, all_isocyanate, all_hydroxyl, isocyanate_value, hydroxyl_values, contents, file_content, capping_group, isocyanate_all, hydroxyl_all)
    
    return right_panel_content_style, main_page_style, hydroxyl_list_style, isocyanate_list_style, right_panel_header_style, main_after_reaction_style, reaction_output_children, left_panel_before_style, left_panel_after_children, successful_upload_children, left_panel_download_style, store_reaction_data


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
            
            return html.A("Download PUR_smiles.txt", href=href, download="PUR_smiles.txt")
    
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
                    mol_block = utils.generate_mol(smiles)
                    mol_filename = f"PUR_{idx + 1}.mol"
                    zipf.writestr(mol_filename, mol_block)

            # Rewind the buffer
            zip_buffer.seek(0)
            href = f"data:application/zip;base64,{base64.b64encode(zip_buffer.read()).decode('utf-8')}"
            return html.A("Download PUR_2D.zip", href=href, download="PUR_2D.zip")
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
                    mol_block = utils.generate_mol2(smiles, idx)
                    mol_filename = f"PUR_{idx + 1}.mol2"
                    zipf.writestr(mol_filename, mol_block)

            # Rewind the buffer
            zip_buffer.seek(0)
            href = f"data:application/zip;base64,{base64.b64encode(zip_buffer.read()).decode('utf-8')}"
            return html.A("Download PUR_3D.zip", href=href, download="PUR_3D.zip")
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
                    conformers_content = utils.generate_conformers(smiles, idx)
                    for conf_num, conformer in enumerate(conformers_content):
                        mol_filename = f"PUR_{idx + 1}_{conf_num}.mol2"
                        zipf.writestr(mol_filename, conformer)

            # Rewind the buffer
            zip_buffer.seek(0)
            href = f"data:application/zip;base64,{base64.b64encode(zip_buffer.read()).decode('utf-8')}"
            return html.A("Download PUR_3D_conformers.zip", href=href, download="PUR_3D_conformers.zip")
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
                    mol_block = utils.generate_image(smiles)
                    mol_filename = f"PUR_{idx + 1}.png"
                    zipf.writestr(mol_filename, mol_block)

            # Rewind the buffer
            zip_buffer.seek(0)
            href = f"data:application/zip;base64,{base64.b64encode(zip_buffer.read()).decode('utf-8')}"
            return html.A("Download PUR_images.zip", href=href, download="PUR_images.zip")
    raise PreventUpdate

# Run the app
if __name__ == '__main__':
    app.run_server(debug=False)
