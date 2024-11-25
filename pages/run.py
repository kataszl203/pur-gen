from fileinput import filename
from typing import Optional

import dash
import pandas as pd
from certifi import contents
import dash_ag_grid as dag
from dash import html, dcc, callback, no_update
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import layouts
import callbacks
import utils

dash.register_page(__name__,
                   path='/run',
                   title='run PUR-GEN',
                   name='run PUR-GEN',
                   image='assets/logo.png')

# Read the compounds
isocyanate_list = [{'label' : i.split(";")[0], 'smiles' : i.split(";")[1]} for i in open("data/isocyanates.txt", "r").read().splitlines()]
hydroxyl_list = [{'label' : i.split(";")[0], 'smiles' : i.split(";")[1]} for i in open("data/poliols.txt", "r").read().splitlines()]
isocyanate_all = [item['smiles'] for item in isocyanate_list]
hydroxyl_all = [item['smiles'] for item in hydroxyl_list]

isocyanate_list_table = [{'label' : list_i['label'], 'smiles' : list_i['smiles'], 'picture': utils.smiles_to_image(list_i['smiles'])} for list_i in isocyanate_list]
hydroxyl_list_table = [{'label' : list_i['label'], 'smiles' : list_i['smiles'], 'picture': utils.smiles_to_image(list_i['smiles'])} for list_i in hydroxyl_list]

defaultColDef_temp = {
    "flex": 1,
    "minWidth": 125,
    "editable": False,
    "filter": True,
    "cellDataType": False,
}

colDef = [
        {"field": "label", "headerName": "NAME",  "checkboxSelection": True, "headerCheckboxSelection": True},
        {"field": "smiles", "headerName": "SMILES"},
        {"field": "picture", "headerName": "PICTURE" , "cellRenderer": "ImgThumbnail",}
    ]

isocyanate_table = dag.AgGrid(
    id="isocyanate-table",
    style={"height": 800, "width": "95%"},
    rowData=isocyanate_list_table,
    columnDefs=colDef,
    defaultColDef=defaultColDef_temp,
    dashGridOptions={
        "pagination": True,

        "rowSelection": "multiple",
        "suppressRowClickSelection": True,
        "rowHeight": 100,
        # "domLayout": "autoHeight"

    },
    columnSize="autoSize",
    columnSizeOptions={"keys": ["picture", "label"]}
)
hydroxyl_table = dag.AgGrid(
    id="hydroxyl-table",
    style={"height": 800, "width": "95%"},
    rowData=hydroxyl_list_table,
    columnDefs=colDef,
    defaultColDef=defaultColDef_temp,
    dashGridOptions={
        "pagination": True,

        "rowSelection": "multiple",
        "suppressRowClickSelection": True,
        "rowHeight": 100,
        # "domLayout": "autoHeight"

    },
    columnSize="autoSize",
    columnSizeOptions={"keys": ["picture", "label"]}
)

modal = dbc.Modal(
    [
        dbc.ModalHeader("Fullscreen Modal"),
        dbc.ModalBody("This is your modal content."),
        dbc.ModalFooter(
            dbc.Button("Close", id="close-modal", className="ml-auto")
        ),
    ],
    id="fullscreen-modal",
    is_open=False,
    fullscreen=True,  # This makes the modal full screen
)

layout = html.Div(style={'display': 'flex'},
    children=[modal,
        html.Div(id = 'left-panel-content',className='run-left-panel-layout',
                       children = [

    html.Div(id = 'left-panel-header',
            children = [html.A(html.Img(src='assets/pur-gen_tg_short_logo.png', 
                                    style={'max-width': '85%', 
                                           'height': 'auto'}), 
                                    href='/'),]),
    html.Div(id = 'left-panel-before-reaction',
            children = [html.H3("SELECT SUBSTRATES",className='run-select-text'),
                        html.H4("Choose at least one isocyanate and one alcohol.",
                                className='run-select-info-text'),
                        layouts.create_switch_with_label('show isocyanates','switch-isocyanate','assets/isocyanates.png'),

                        layouts.create_switch_with_label('show alcohols','switch-hydroxyl','assets/alcohols.png'),

                        #layouts.create_upload_component(),
                        dcc.Store(id='store-substrates'),
                        layouts.create_texarea_component(),
                        layouts.create_select_size_component(),
                        layouts.create_capping_group_component(),

                        html.Div([dcc.Link(html.Button("RUN",
                            className='button button',
                            n_clicks=0),id='make-oligomers-button',href='')], 
                            style = {'display':'flex', 
                                     'justify-content': 'center',
                                     'margin-top':'50px',
                                     'margin-bottom':'50px'})]),
                        dcc.Store(id="custom-compounds"),
                        dcc.Store(id='store-reaction'),
                       dcc.Store(id='store-text-input')]),
              html.Div([
                  html.Div(id = 'right-panel-content',
                           children = [#layouts.create_checkbox_list(isocyanate_list, isocyanate_all, "Select isocyanates: ", 'isocyanate-list', 'select-all-isocyanate', 'isocyanate-list-checkbox'),
                                        html.Div([
                                            dbc.Row([
                                                dbc.Col([
                                                dbc.Row([html.H3("Select isocyanates: ", className='highlighted-left-text', id="isocyanate-table-label"),]),
                                                dbc.Row([isocyanate_table,]),
                                            ], id ="isocyanate-table-div", style={"margin-right": "0px", "margin-left": "0px"} ),

                                            dbc.Col([
                                                dbc.Row([html.H3("Select alcohols:", className='highlighted-left-text', id="hydroxyl-table-label"),]),
                                                dbc.Row([hydroxyl_table,]),
                                            ], id="hydroxyl-table-div", style={"margin-right": "0px", "margin-left": "0px"}   ), ]),
                                            dbc.Modal(id="isocyanate-modal", size="md", centered=True, ),
                                            dbc.Modal(id="alcohol-modal", size="md", centered=True, )
                                        ], ),
                                       #layouts.create_checkbox_list(hydroxyl_list, hydroxyl_all, "Select alcohols:", 'hydroxyl-list', 'select-all-hydroxyl', 'hydroxyl-list-checkbox'),

                                       ],
                           style={})],
                       style={'flex': '2'}),
              ])

@callback(Output('upload-substrates-textarea', 'value'),
          Output('sample-input-button', 'n_clicks'),
          Input('sample-input-button', 'n_clicks'),
          prevent_initial_call=True)
def insert_sample_input(n_clicks):
    text_input: str
    if n_clicks > 0:
        with open('static/sample_input.txt', 'r') as f:
            text_input = f.read()
    return text_input, n_clicks-1

@callback(Output('character_count_indicator', 'children'),
          Input('upload-substrates-textarea', 'value'))
def count_characters(value: Optional[str]):
    if value is None:
        value = ''
    return html.Label(children=[f"Characters: {len(value)}/2000"], className='run-char-count-text')


# Define callback to show substrates lists
@callback(#Output('hydroxyl-list', 'style'),
        #Output('isocyanate-list', 'style'),
        Output('hydroxyl-table-label', 'style'),
        Output('isocyanate-table-label', 'style'),
        Output('hydroxyl-table', 'style'),
        Output('isocyanate-table', 'style'),
        Input('switch-hydroxyl','on'),
        Input('switch-isocyanate','on'))
def show_substrates(hydroxyl_clicks,isocyanate_clicks):
    if isocyanate_clicks and hydroxyl_clicks:
        hydroxyl_list_style = {'display':'block','flex': '1', 'padding': '10px', "margin-right": "5px"}
        hydroxyl_table_style = {'display':'block', "height": "800px", "margin-right": "5px"}
        isocyanate_list_style = {'display':'block','flex': '1', 'padding': '10px', "margin-right": "5px"}
        isocyanate_table_style = {'display':'block', "height": "800px", "margin-right": "5px"}
    
    elif isocyanate_clicks:       
        hydroxyl_list_style = {'display':'none'}
        hydroxyl_table_style = {'display': 'none'}
        isocyanate_list_style = {'display':'block','flex': '1', 'padding': '10px', "margin-right": "5px"}
        isocyanate_table_style = {'display': 'block', "height": "800px", "margin-right": "5px"}

    elif hydroxyl_clicks:        
        hydroxyl_list_style = {'display':'block','flex': '1', 'padding': '10px', "margin-right": "5px"}
        hydroxyl_table_style = {'display': 'block', "height": "800px", "margin-right": "5px"}
        isocyanate_list_style = {'display':'none'}
        isocyanate_table_style = {'display': 'none'}
    
    else:
        hydroxyl_list_style = {'display':'none'}
        hydroxyl_table_style = {'display': 'none'}
        isocyanate_list_style = {'display':'none'}
        isocyanate_table_style = {'display': 'none'}

    #return hydroxyl_list_style, isocyanate_list_style, hydroxyl_table_style, isocyanate_table_style
    return hydroxyl_list_style, isocyanate_list_style, hydroxyl_table_style, isocyanate_table_style

#Select all
@callback(
    Output('isocyanate-list-checkbox', 'value'),
    Output('hydroxyl-list-checkbox', 'value'),
    Input('select-all-isocyanate', 'value'),
    Input('select-all-hydroxyl', 'value'),
    State('isocyanate-list-checkbox', 'options'),
    State('hydroxyl-list-checkbox', 'options'),
)
def select_all_none(select_all_isocyanate_value, select_all_hydroxyl_value,
                    options_isocyanate, options_hydroxyl):
    all_isocyanate = []
    all_hydroxyl = []
    all_isocyanate = [option["value"] for option in options_isocyanate if select_all_isocyanate_value]
    all_hydroxyl = [option["value"] for option in options_hydroxyl if select_all_hydroxyl_value]
    return all_isocyanate, all_hydroxyl


#Info regarding substrates depending on size
@callback(
        Output('size-info', 'children'),
        Input('select-size', 'value')
)

def info_about_size(size):
    if size == '3':
        return ['Choose at least one diisocyanate or at least one diol.']
    elif size == '4':
        return ['Choose at least one diisocyanate and at least one diol.']


@callback(Output('load-output-log', 'value'),
          Output('load-output-log', 'style'),
          Output("custom-compounds", "data"),
          Input("apply-text-input-button", "n_clicks"),
          State('upload-substrates-textarea', 'value'),
          prevent_initial_call=True)
def load_text_input(nclicks, text, ):
    msg, uploaded_substrates, success, failed_substrates = callbacks.validate_text_input(text)
    not_classified_smiles: list
    reaction, info, iso_mols, poliol_mols, not_classified_smiles = utils.prepare_reaction(uploaded_substrates)
    if not_classified_smiles is not None and len(not_classified_smiles) > 0:
        msg += f"\nFollowing SMILES have not been classified, therefore will not be used further: \n"
        for ncs in not_classified_smiles:
            msg += f"{ncs}, "
            uploaded_substrates.remove(ncs)
    style = {
                        'display': 'block',
                        'width': '100%',
                        'resize': 'none',
                        'whiteSpace': 'pre',
                        "margin-right": "0px",
                    }
    return msg, style,uploaded_substrates

@callback(Output('grid-cell-loaded-components', 'rowData'),
          Output('make-oligomers-button', 'href'),
Output('stored-substrates', 'data'),
          Input("custom-compounds", "data"),
          Input("hydroxyl-table", "selectedRows"),
          Input("isocyanate-table", "selectedRows")
        #Input('isocyanate-list-checkbox', 'value'),
        #Input('hydroxyl-list-checkbox', 'value'),
          )
def fill_loaded_data(custom_compounds, hydroxyl_checkbox_value, isocyanate_checkbox_value):
    images = []
    substrate_type = []
    if not custom_compounds:
        custom_compounds = []
    if not isocyanate_checkbox_value:
        isocyanate_checkbox_value = []
    if not hydroxyl_checkbox_value:
        hydroxyl_checkbox_value = []
    smiles = []
    for icv in isocyanate_checkbox_value:
        smiles.append(icv["smiles"])
    for hcv in hydroxyl_checkbox_value:
        smiles.append(hcv["smiles"])
    #smiles = isocyanate_checkbox_value + hydroxyl_checkbox_value
    for substrate in custom_compounds:
        if substrate not in smiles:
            smiles.append(substrate)
    for element in smiles:
        images.append(utils.smiles_to_image(element))
    reaction, info, iso_mols, poliol_mols, not_classified_smiles = utils.prepare_reaction(smiles)
    temp = []
    for mol in iso_mols:
        temp.append(mol)
    for mol in poliol_mols:
        temp.append(mol)
    for t in temp:
        substrate_type.append(t.GetProp('func_group'))
    products_df = pd.DataFrame({'index': pd.Index(range(1, len(smiles) + 1)), 'smiles': smiles, "picture": images, "substrate_type": substrate_type})
    link = '/results'
    if not smiles:
        link = ""
    return products_df.to_dict('records'), link, smiles

# Define callback to store size and capping groups
@callback(Output('stored-size', 'data'),
          Output('stored-capping', 'data'),
          Input('select-size', 'value'),
          Input('capping-group', 'value') 
          )

def store_size_and_capping(size_value, capping_value):
    return size_value, capping_value

@callback(
    Output("img-modal", "is_open"),
    Output("img-modal", "children"),
    Input("grid-cell-loaded-components", "cellRendererData"),
)
def show_change(data):
    if data:
        return True, html.Img(src='data:image/jpeg;base64,' + data["value"])
    return False, None


"""
@callback(
    Output("fullscreen-modal", "is_open"),
    [Input("apply-text-input-button", "n_clicks"), Input("close-modal", "n_clicks")],
    [State("fullscreen-modal", "is_open")],
)
def toggle_modal(load_clicks, close_clicks, is_open):
    if load_clicks or close_clicks:
        return not is_open
    return is_open"""

@callback(
    Output("isocyanate-modal", "is_open"),
    Output("isocyanate-modal", "children"),
    Input("isocyanate-table", "cellRendererData"),
)
def show_change_isocyanate(data):
    if data:
        return True, html.Img(src='data:image/jpeg;base64,' + data["value"])
    return False, None

@callback(
    Output("alcohol-modal", "is_open"),
    Output("alcohol-modal", "children"),
    Input("hydroxyl-table", "cellRendererData"),
)
def show_change_alcohol(data):
    if data:
        return True, html.Img(src='data:image/jpeg;base64,' + data["value"])
    return False, None