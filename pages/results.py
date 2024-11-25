import dash
from dash import html, dcc, callback, dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import callbacks
import utils
import pandas as pd
import io
import zipfile
import tempfile
import dash_ag_grid as dag

dash.register_page(__name__,
                   path='/results',
                   title='results PUR-GEN',
                   name='results PUR-GEN',
                   image='assets/logo.png')
columnDefs_temp = [
        {"field": "Compound", "headerName": "INDEX", 'cellDataType': 'number'},
        {"field": "SMILES", },
        {"field": "Molecular Weight", 'cellDataType': 'number'},
        {"field": "Heavy Atoms", 'cellDataType': 'number'},
        {"field": "Rotatable Bonds", 'cellDataType': 'number'},
        {"field": "Ester bond"},
        {"field": "Ether bond"},
        {"field": "Aromatic Atoms", 'cellDataType': 'number'},
        {"field": "Aromatic Proportion", 'cellDataType': 'number'},
        {"field": "clogP", 'cellDataType': 'number'},
        {"field": "TPSA", 'cellDataType': 'number'},
        {"field": "MR", 'cellDataType': 'number'},
        {"field": "picture", "headerName": "PICTURE", "cellRenderer": "ImgThumbnail", }
    ]
defaultColDef_temp = {
    "flex": 1,
    "minWidth": 125,
    "editable": False,
    "filter": True,
    "cellDataType": False,
}
pur_table = dag.AgGrid(
    id="grid-cell-loaded-components-results-pur",
    style={"height": 800, "width": "100%"},
    rowData=[],
    columnDefs=columnDefs_temp,
    defaultColDef=defaultColDef_temp,
    dashGridOptions={'pagination': True, "rowHeight": 100, "paginationPageSize": 20, "columnHoverHighlight": True},
    columnSize="autoSize",
    # columnSizeOptions={"keys": ["picture"]}
)
pur_modal = dbc.Modal(id="img-modal-3", size="md", centered=True, )

columnDefs = [
        {"field": "index", "headerName": "INDEX",},
        {"field": "smiles", "headerName": "SMILES"},
        {"field": "substrate_type", "headerName": "TYPE"},
        {"field": "picture", "headerName": "PICTURE" , "cellRenderer": "ImgThumbnail",}
    ]
columnDefsDownload = [
        {"field": "Compound", "headerName": "INDEX",  "checkboxSelection": True, "headerCheckboxSelection": True},
        {"field": "SMILES", "headerName": "SMILES"},
        {"field": "picture", "headerName": "PICTURE" , "cellRenderer": "ImgThumbnail",}
    ]
defaultColDef = {
    "flex": 1,
    "minWidth": 125,
    "editable": False,
    "filter": True,
    "cellDataType": False,
}

defaultColDefDownload = {
    "flex": 1,
    "editable": False,
    "filter": True,
    "cellDataType": False,
    """"checkboxSelection": {
        "function": 'params.column == params.columnApi.getAllDisplayedColumns()[0]'
    },
    "headerCheckboxSelection": {
        "function": 'params.column == params.columnApi.getAllDisplayedColumns()[0]'
    },"""
    "minWidth": 125,
}
pur_modal2 = dbc.Modal(id="img-modal-5", size="md", centered=True, )
modal2 = dbc.Modal(
    [
        dbc.ModalHeader([html.H3('DOWNLOAD RESULTS', className='highlighted-left-text-margin-2'),]),
        dbc.ModalBody([
                html.Div(className='results-buttons', children=[
                    dbc.Row([
                        dbc.Col(
                            [
                                dbc.Stack([
                                    dbc.Row([html.Div(style={'margin-bottom': '10px'}, children=[
                                        dcc.Loading(id='loading-2d', type='circle', children=[
                                            html.Button('2D STRUCTURES (.mol)', id='generate-2d', n_clicks=0, style={
                                                'width': '100%'
                                            }),
                                            dcc.Download(id="download-2d")
                                        ],
                                            color="#b292f3",
                                            delay_show=500,
                                            delay_hide=500,)
                                    ]),]),
                                    dbc.Row([html.Div(style={'margin-bottom': '10px'}, children=[
                                        dcc.Loading(id='loading-3d', type='circle', children=[
                                            html.Button('3D STRUCTURES (.mol2)', id='generate-3d', n_clicks=0, style={
                                                'width': '100%'
                                            }),
                                            dcc.Download(id='download-3d')
                                        ],
                                            color="#b292f3",
                                            delay_show=500,
                                            delay_hide=500,)
                                    ]),]),
                                    dbc.Row([html.Div(style={'margin-bottom': '10px'}, children=[
                                        dcc.Loading(id='loading-conformers', type='circle', fullscreen=False, children=[
                                            html.Button('3D CONFORMERS (.mol2)', id='generate-conformers', n_clicks=0, style={
                                                'width': '100%'
                                            }),
                                            dcc.Download(id='download-conformers')
                                        ],
                                            color="#b292f3",
                                            delay_show=500,
                                            delay_hide=500,
                                            style={
                                                'alignItem': 'left',
                                            })
                                    ]),]),
                                    dbc.Row([html.H5("Generation of conformers may take longer, especially with numerous compounds.",
                                            className='run-select-info-text2', ),]),
                                    dbc.Row([html.Div(style={'margin-bottom': '10px'}, children=[
                                        dcc.Loading(
                                            id='loading-csv',
                                            type='circle',
                                            children=[
                                            html.Button('PROPERTIES (.csv)', id='generate-csv', n_clicks=0, style={
                                                'width': '100%'
                                            }),
                                            dcc.Download(id="download-csv")
                                        ],
                                            color="#b292f3",
                                            delay_show=500,
                                            delay_hide=500,
                                            style={
                                                'text-align': 'left',
                                            }
                                        )
                                    ])]),
                                ], gap=2)
                            ], width=4
                        ),
                        dbc.Col(
                            [
                                pur_modal2,
                                dag.AgGrid(
                                    id="grid-cell-loaded-components-download-results",
                                    columnDefs=columnDefsDownload,
                                    defaultColDef=defaultColDefDownload,
                                    dashGridOptions={
                                        "pagination": True,

                                        "rowSelection": "multiple",
                                        "suppressRowClickSelection": True,
                                        "rowHeight": 100,
                                        #"domLayout": "autoHeight"

                                    },
                                    columnSize="autoSize",
                                    columnSizeOptions={"keys":["Compound", "picture"]},
                                    style={
                                        "ag-selected-row-background-color": "#b292f3",
                                        "ag-selected-column-background-color": "#b292f3"
                                    }
                                )
                            ], width={"size": 7, "order": "last", "offset": 1},
                        ),
                    ]),
                    html.Div(id="selected-rows-output")
                ],
                         style={
                             #'width': '420px'
                         })
            ]),
        dbc.ModalFooter(
            html.Button('Close', id='close-modal2', n_clicks=0, style={
                                            'width': '200px'
                                        }),
        ),
    ],
    id="fullscreen-modal-1",
    is_open=False,
    size="xl", centered=True,
)

layout = dcc.Loading(
    id="global-loading",
    overlay_style={"visibility":"visible", "filter": "blur(2px)"},
    type="circle",
    color="#b292f3",
    delay_show=500,
    delay_hide=500,
    #fullscreen=True,
    children=html.Div(id='results-page', style={'display': 'block'}, children=[
        modal2,
        html.Center(style={'alignItems': 'center', 'background-color': '#F0F0F0', 'margin-top': '20px'},
                    children=[
                        html.A(html.Img(src='assets/pur-gen_tg_full_logo.png', className='homepage-logo'), href='/')
                    ]),
        html.Div(style={'display': 'flex',}, children=[
            html.Div(style={'flex': '1'}, children=[
                html.H3('INPUT STRUCTURES AND PARAMETERS', className='highlighted-left-text-margin'),
                html.Div(id='summary-output'),

            ],),
            html.Div(style={'flex': '2', "margin-left": "20px"}, children=[
        html.H3("UPLOADED SUBSTRATES", className='highlighted-left-text-margin'),
        dag.AgGrid(
            id="grid-cell-loaded-components-results",
            columnDefs=columnDefs,
            defaultColDef=defaultColDef,
            dashGridOptions={'pagination': True, "rowHeight": 100, },
            columnSize="autoSize",
            columnSizeOptions={"keys":["index", "picture", "substrate_type"]},
            style={"width": "100%", "ag-selected-row-background-color": "#b292f3", "ag-selected-column-background-color": "#b292f3"}
        ),
        dbc.Modal(id="img-modal-2", size="md", centered=True,),
            ])
        ]),
        dcc.Store(id='conformers_generated'),
        dcc.Store(id='products'),
        dcc.Store(id='structures-store'),
        dcc.Store(id='table-store', storage_type='local'),
        dcc.Store(id='downloadable-rows', storage_type='local'),
        dcc.Store(id='table-store-todownload', storage_type='local'),
        dcc.Store(id='table-store-todownload-final', storage_type='local'),
        dcc.Store(id='fig-store'),
        html.H1('GENERATED PUR FRAGMENTS', className='highlighted-center-text'),
        dcc.Tabs(id="tabs", value='tab-structures', children=[
            dcc.Tab(label='PUR structures', value='tab-structures', selected_style={
                'borderTop': '2px solid #b292f3',
                'color': 'gray',
                'font-weight': 'bold',
            }, style={
                'color': 'gray',
                'font-weight': 'normal',
            }),
            dcc.Tab(label='Calculated properties', value='tab-table', selected_style={
                'borderTop': '2px solid #b292f3',
                'color': 'gray',
                'font-weight': 'bold',
            }, style={
                'color': 'gray',
                'font-weight': 'normal',
            }),
            dcc.Tab(label='Properties histograms', value='tab-histograms', selected_style={
                'borderTop': '2px solid #b292f3',
                'color': 'gray',
                'font-weight': 'bold',
            }, style={
                'color': 'gray',
                'font-weight': 'normal',
            })
        ]),
        dcc.Loading(
            id="loading-tabs-content",
            type="circle",
            children=[
                html.Div(id='tabs-output')
            ],
            overlay_style={"visibility": "visible", "filter": "blur(2px)"},
            color="#b292f3",
            delay_show=100,
            delay_hide=100,
        )
    ]),
    target_components={
        'summary-output': 'children',

    }
)

# Prepare data when page loads
def prepare_data(stored_substrates, stored_size, stored_capping):
    summary, structures_imgs, capped_products = callbacks.show_reactions(stored_substrates, stored_size, stored_capping)
    products_df = pd.DataFrame({'Compound': pd.Index(range(1, len(capped_products) + 1)), 'SMILES': capped_products})
    compounds_properties_df = utils.calculate_properties_df(products_df)
    fig = utils.generate_properties_figure(compounds_properties_df)
    images = []
    for element in capped_products:
        images.append(utils.smiles_to_image(element))
    compounds_properties_df["picture"] = images
    table = dash_table.DataTable(
        compounds_properties_df.to_dict('records'),
        style_data={'textAlign': 'left'},
        style_header={'textAlign': 'left'}
    )
    compounds_properties_df_2 = compounds_properties_df
    compounds_properties_df_2['select'] = True
    return summary, structures_imgs, table, fig, compounds_properties_df.to_dict('records'), compounds_properties_df_2.to_dict('records')


@callback(
    Output('structures-store', 'data'),
    Output('table-store', 'data'),
    Output('fig-store', 'data'),
    Output('summary-output', 'children'),
    Output('table-store-todownload', 'data'),
    #
    #Output('conformers-generated', 'data'),
    Input('stored-substrates', 'data'),
    Input('stored-size', 'data'),
    Input('stored-capping', 'data')
)
def initialize_data(stored_substrates, stored_size, stored_capping):
    summary, structures_imgs, table, fig, compounds_data, compounds_data_df = prepare_data(stored_substrates, stored_size, stored_capping)
    fig_data = fig.to_plotly_json()
    return structures_imgs, compounds_data, fig_data, summary, compounds_data_df

@callback(Output('grid-cell-loaded-components-results', 'rowData'),
    Input('stored-substrates', 'data'))
def init_uploaded_substrates(stored_substrates):
    images = []
    substrate_type = []
    for element in stored_substrates:
        images.append(utils.smiles_to_image(element))
    reaction, info, iso_mols, poliol_mols, not_classified_smiles = utils.prepare_reaction(stored_substrates)
    temp = iso_mols + poliol_mols
    for t in temp:
        substrate_type.append(t.GetProp('func_group'))
    products_df2 = pd.DataFrame(
        {'index': pd.Index(range(1, len(stored_substrates) + 1)), 'smiles': stored_substrates, "picture": images, "substrate_type": substrate_type})
    return  products_df2.to_dict('records')

@callback(Output('grid-cell-loaded-components-download-results', 'rowData'),
    Input('table-store-todownload', 'data'))
def init_download_substrates(stored_substrates):
    return stored_substrates

@callback(
    Output("selected-rows-output", "children"),  # Output to display selected rows
    Output("downloadable-rows", "data"),
    Input("grid-cell-loaded-components-download-results", "selectedRows"),  # Input to monitor row selection
)
def display_selected_rows(selected_rows):
    if not selected_rows:
        return "No rows selected!", selected_rows
    # Display the selected rows as a list of dictionaries
    return f"Selected Rows: {len(selected_rows)}", selected_rows

@callback(Output("grid-cell-loaded-components-results-pur", "rowData"),
          Input('table-store', 'data'),)
def load_table_data(table_data):
    return table_data


@callback(
    Output('tabs-output', 'children'),
    Input('tabs', 'value'),
    Input('structures-store', 'data'),
    Input('table-store', 'data'),
    Input('fig-store', 'data')
)
def process_substrates(tab, structures_imgs, table_data, fig_data):
    if tab == 'tab-structures':
        tab_output = structures_imgs
    elif tab == 'tab-table':
        """"
        table = dash_table.DataTable(
            table_data,
            style_data={'textAlign': 'left'},
            style_header={'textAlign': 'left'}
        )
        """

        tab_output = html.Div(children=[
            html.Center(html.H4('''Calculated PUR fragments properties:
                molecular weight, heavy atom count, number of rotatable bonds, 
                presence of ester and ether bonds, count of aromatic atoms, aromatic proportion 
                (ratio of aromatic atoms to heavy atoms), Crippen-Wildman partition coefficient 
                (cLogP), topological polar surface area 
                (TPSA) and Crippen-Wildman molar refraction (MR).''',
                                className='results-properties-description')),
            pur_table,
            pur_modal,
            html.Br()
        ])
    elif tab == 'tab-histograms':
        tab_output = html.Div(children=[
            html.Center(html.H4('''Calculated PUR fragments properties:
                molecular weight, heavy atom count, number of rotatable bonds, 
                presence of ester and ether bonds, count of aromatic atoms, aromatic proportion 
                (ratio of aromatic atoms to heavy atoms), Crippen-Wildman partition coefficient 
                (cLogP), topological polar surface area 
                (TPSA) and Crippen-Wildman molar refraction (MR).''',
                                className='results-properties-description')),
            dcc.Graph(figure=fig_data)
        ])

    return tab_output


@callback(
    Output('download-csv', 'data'),
    Input('generate-csv', 'n_clicks'),
    State('downloadable-rows', 'data'),
    prevent_initial_call=True
)
def download_csv(n_clicks, table_data):
    if n_clicks and table_data:  # Ensure table_data is passed
        df = pd.DataFrame(table_data)
        df.drop(["select", "picture"], axis=1, inplace=True)
        return dcc.send_data_frame(df.to_csv, "properties.csv", index=False)


@callback(
    Output('download-2d', 'data'),
    Input('generate-2d', 'n_clicks'),
    State('downloadable-rows', 'data'),
    prevent_initial_call=True
)
def download_mol(n_clicks, table_data):
    if n_clicks and table_data:  # Ensure table_data is passed
        df = pd.DataFrame(table_data)
        smiles_list = df['SMILES'].values
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
            for idx, smiles in enumerate(smiles_list):
                mol_block = utils.generate_mol(smiles)
                mol_filename = f"PUR_{idx + 1}.mol"
                zipf.writestr(mol_filename, mol_block)
        zip_buffer.seek(0)
        return dcc.send_bytes(zip_buffer.getvalue(), "PUR_2D.zip")


@callback(
    Output('download-3d', 'data'),
    Input('generate-3d', 'n_clicks'),
    State('downloadable-rows', 'data'),
    prevent_initial_call=True
)
def download_mol_3d(n_clicks, table_data):
    if n_clicks and table_data:  # Ensure table_data is passed
        df = pd.DataFrame(table_data)
        smiles_list = df['SMILES'].values
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
            for idx, smiles in enumerate(smiles_list):
                mol_block = utils.generate_mol2(smiles, idx)
                mol_filename = f"PUR_{idx + 1}.mol2"
                zipf.writestr(mol_filename, mol_block)
        zip_buffer.seek(0)
        with tempfile.NamedTemporaryFile(delete=True) as tmp_file:
            tmp_file.write(zip_buffer.getvalue())
            tmp_file_name = tmp_file.name
            return dcc.send_file(tmp_file_name, filename="PUR_3D.zip")


@callback(
    Output('download-conformers', 'data'),
    Input('generate-conformers', 'n_clicks'),
    State('downloadable-rows', 'data'),
    prevent_initial_call=True
)
def download_conformers(n_clicks, conformers_content):
    if n_clicks and conformers_content:  # Ensure table_data is passed
        df = pd.DataFrame(conformers_content)
        smiles_list = df['SMILES'].values
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
            for idx, smiles in enumerate(smiles_list):
                conformers_content = utils.generate_conformers(smiles, idx)
                for conf_num, conformer in enumerate(conformers_content):
                    mol_filename = f"PUR_{idx + 1}_{conf_num}.mol2"
                    zipf.writestr(mol_filename, conformer)
        zip_buffer.seek(0)
        return dcc.send_bytes(zip_buffer.getvalue(), "PUR_conformers.zip")

@callback(
    Output("fullscreen-modal-1", "is_open"),
    [Input('download-generated-data', 'n_clicks'), Input("close-modal2", "n_clicks")],
    [State("fullscreen-modal-1", "is_open")],
prevent_initial_call=True,
    surpress_callback_exceptions=True
)
def toggle_modal(load_clicks, close_clicks, is_open):
    if load_clicks or close_clicks:
        return not is_open
    return is_open

@callback(
    Output("img-modal-2", "is_open"),
    Output("img-modal-2", "children"),
    Input("grid-cell-loaded-components-results", "cellRendererData"),
)
def show_change(data):
    if data:
        return True, html.Img(src='data:image/jpeg;base64,' + data["value"])
    return False, None

@callback(
    Output("img-modal-3", "is_open"),
    Output("img-modal-3", "children"),
    Input("grid-cell-loaded-components-results-pur", "cellRendererData"),
)
def show_change2(data):
    if data:
        return True, html.Img(src='data:image/jpeg;base64,' + data["value"])
    return False, None

@callback(
    Output("img-modal-5", "is_open"),
    Output("img-modal-5", "children"),
    Input("grid-cell-loaded-components-download-results", "cellRendererData"),
)
def show_change3(data):
    if data:
        return True, html.Img(src='data:image/jpeg;base64,' + data["value"])
    return False, None