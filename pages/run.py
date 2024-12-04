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

buttons = dbc.Row(
    [
        dbc.Col(
            dbc.Button(
                "Home",
                color="primary",
                href="/",
                className='button',  # Single 'button' class for CSS
                n_clicks=0
            ),
            width="auto",
        ),
        dbc.Col(
            dbc.Button(
                "How to Use",
                href="/how-to-use",
                color="primary",
                className='button',  # Single 'button' class for CSS
                n_clicks=0
            ),
            width="auto",
        )
    ],
    className="button-row flex-nowrap",  # Custom class for styling the button row
    align="center",
)

# Navbar layout with logo and toggler
navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.Row(
                [

                    dbc.Col(
                        dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
                        className="d-md-none",  # Show toggler only on smaller screens
                    ),
                ],
                className="g-0 w-100 align-items-center",
                justify="between",  # Spread image and buttons
            ),
            dbc.Collapse(
                buttons,
                id="navbar-collapse",
                is_open=False,
                navbar=True,
                className="justify-content-end",  # Align buttons to the far right
            ),
        ],
        fluid=True,  # Allow full-width layout
    ),
    className="navbar-dark",
    fixed="top",
)


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
    persistence=True,
    persistence_type='local',
    persisted_props=['value', 'selectedRows'],
    columnSize="sizeToFit",
    #columnSizeOptions={"keys": ["picture", "label"]}
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
    persistence=True,
    persistence_type='local',
    persisted_props=['value', 'selectedRows'],
    columnSize="sizeToFit",
    #columnSizeOptions={"keys": ["picture", "label"]}
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

warning = dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Please select at least one alcohol and isocyanate!")),
                dbc.ModalBody("In order to proceed, you need to select at least one alcohol and one isocyanate."),
            ],
            id="warning-modal",
            is_open=False,
            centered=True,
        )

layout = html.Div([
navbar, warning,
html.Div(style={'display': 'flex', 'margin-top': '60px'},
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
                        dcc.Store(id='store-substrates', storage_type='local'),
                        layouts.create_texarea_component(),
                        layouts.create_select_size_component(),
                        layouts.create_capping_group_component(),

                        html.Div([dcc.Link(html.Button("CALCULATE PRODUCTS",
                            className='button button',
                            n_clicks=0, id="run-button"),id='make-oligomers-button',href='')],
                            style = {'display':'flex',
                                     'justify-content': 'center',
                                     'margin-top':'50px',
                                     'margin-bottom':'50px'})]),
                        dcc.Store(id="custom-compounds", storage_type='local'),
                        dcc.Store(id='store-reaction', storage_type='local'),
                       dcc.Store(id='store-text-input', storage_type='local')]),
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
])

@callback(Output('upload-substrates-textarea', 'value'),
          Output('sample-input-button', 'n_clicks'),
          Input('sample-input-button', 'n_clicks'),
        Input("clear-text-input-button", "n_clicks"),
          prevent_initial_call=True)
def insert_sample_input(n_clicks, nclicks2):
    text_input: str = ""

    if n_clicks > 0:
        with open('static/sample_input_v2.txt', 'r') as f:
            text_input = f.read()

    return text_input, 0

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
          Output("clear-text-input-button", "n_clicks"),
          Input("apply-text-input-button", "n_clicks"),
          Input("clear-text-input-button", "n_clicks"),
          State('upload-substrates-textarea', 'value'),
          prevent_initial_call=True
          )
def load_text_input(nclicks, nclicks_clear, text):
    style = {
        'display': 'block',
        'width': '100%',
        'resize': 'none',
        'whiteSpace': 'pre',
        "margin-right": "0px",
    }
    if nclicks_clear>0:
        return "Cleared input", style, [], 0
    msg, uploaded_substrates, success, failed_substrates = callbacks.validate_text_input(text)
    not_classified_smiles: list
    reaction, info, iso_mols, poliol_mols, not_classified_smiles = utils.prepare_reaction(uploaded_substrates)
    if not_classified_smiles is not None and len(not_classified_smiles) > 0:
        msg += f"\nFollowing SMILES have not been classified, therefore will not be used further: \n"
        for ncs in not_classified_smiles:
            msg += f"{ncs}, "
            uploaded_substrates.remove(ncs)

    return msg, style,uploaded_substrates, 0

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
    substrate_type_custom = []
    if not custom_compounds:
        custom_compounds = []
    if not isocyanate_checkbox_value:
        isocyanate_checkbox_value = []
    if not hydroxyl_checkbox_value:
        hydroxyl_checkbox_value = []
    smiles = []
    smiles_custom = []
    for icv in isocyanate_checkbox_value:
        smiles.append(icv["smiles"])
    for hcv in hydroxyl_checkbox_value:
        smiles.append(hcv["smiles"])
    reaction, info, iso_mols, poliol_mols, not_classified_smiles = utils.prepare_reaction(smiles)
    temp = []
    for mol in iso_mols:
        temp.append(mol)
    for mol in poliol_mols:
        temp.append(mol)
    #smiles = isocyanate_checkbox_value + hydroxyl_checkbox_value
    for t in temp:
        substrate_type.append(t.GetProp('func_group'))

    for element in smiles:
        images.append(utils.smiles_to_image(element))

    products_df_normal = pd.DataFrame({'index': pd.Index(range(1, len(smiles) + 1)), 'smiles': smiles, "picture": images,
                                "substrate_type": substrate_type})

    for substrate in custom_compounds:
        if substrate not in smiles:
            smiles_custom.append(substrate)
    reaction, info, iso_mols_cst, poliol_mols_cst, not_classified_smiles = utils.prepare_reaction(smiles_custom)
    temp = []
    for mol in iso_mols_cst:
        temp.append(mol)
    for mol in poliol_mols_cst:
        temp.append(mol)
    for t in temp:
        substrate_type_custom.append(t.GetProp('func_group'))
    images_custom = []
    for element in smiles_custom:
        images_custom.append(utils.smiles_to_image(element))
    products_df = pd.DataFrame()
    products_df_custom = pd.DataFrame({'index': pd.Index(range(len(smiles) + 1, len(smiles) + 1 + len(smiles_custom))), 'smiles': smiles_custom, "picture": images_custom, "substrate_type": substrate_type_custom})
    if not products_df_custom.empty and not products_df_normal.empty:
        products_df = pd.concat([products_df_normal, products_df_custom], axis=0)
    elif not products_df_normal.empty:
        products_df = products_df_normal
    elif not products_df_custom.empty:
        products_df = products_df_custom
    link = '/results'
    if not smiles and not smiles_custom:
        link = ""
    for sc in smiles_custom:
        smiles.append(sc)
    if not iso_mols_cst and not iso_mols:
        link = ""
    if not poliol_mols_cst and not poliol_mols:
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


@callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@callback(
    Output("warning-modal", "is_open"),
    [Input("run-button", "n_clicks")],
    [State('make-oligomers-button', 'href')],
    prevent_initial_call=True)
def show_warning_modal(nclicks, data):
    if data == "" and nclicks>0:
        return True
    return False