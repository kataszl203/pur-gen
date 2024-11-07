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

dash.register_page(__name__,
                   path='/results',
                   title='results PUR-GEN',
                   name='results PUR-GEN',
                   image='assets/logo.png')

layout = dcc.Loading(
    id="global-loading",
    overlay_style={"visibility":"visible", "filter": "blur(2px)"},
    type="circle",
    color="#b292f3",
    delay_show=500,
    delay_hide=500,
    #fullscreen=True,
    children=html.Div(id='results-page', style={'display': 'block'}, children=[
        html.Center(style={'alignItems': 'center', 'background-color': '#F0F0F0', 'margin-top': '20px'},
                    children=[
                        html.A(html.Img(src='assets/pur-gen_tg_full_logo.png', className='homepage-logo'), href='/')
                    ]),
        html.Div(style={'display': 'flex'}, children=[
            html.Div(style={'flex': '1'}, children=[
                html.H3('INPUT STRUCTURES AND PARAMETERS', className='highlighted-left-text-margin'),
                html.Div(id='summary-output')
            ]),
            html.Div(style={'flex': '1'}, children=[
                html.H3('DOWNLOAD RESULTS', className='highlighted-left-text-margin'),
                html.Div(className='results-buttons', children=[
                    html.Div(style={'margin-bottom': '10px'}, children=[
                        dcc.Loading(id='loading-2d', type='circle', children=[
                            html.Button('2D STRUCTURES (.mol)', id='generate-2d', n_clicks=0, style={
                                'width': '400px'
                            }),
                            dcc.Download(id="download-2d")
                        ],
                            color="#b292f3",
                            delay_show=500,
                            delay_hide=500,)
                    ]),
                    html.Div(style={'margin-bottom': '10px'}, children=[
                        dcc.Loading(id='loading-3d', type='circle', children=[
                            html.Button('3D STRUCTURES (.mol2)', id='generate-3d', n_clicks=0, style={
                                'width': '400px'
                            }),
                            dcc.Download(id='download-3d')
                        ],
                            color="#b292f3",
                            delay_show=500,
                            delay_hide=500,)
                    ]),
                    html.Div(style={'margin-bottom': '10px'}, children=[
                        dcc.Loading(id='loading-conformers', type='circle', fullscreen=False, children=[
                            html.Button('3D CONFORMERS (.mol2)', id='generate-conformers', n_clicks=0, style={
                                'width': '400px'
                            }),
                            dcc.Download(id='download-conformers')
                        ],
                            color="#b292f3",
                            delay_show=500,
                            delay_hide=500,
                            style={
                                'alignItem': 'left',
                            })
                    ]),
                    html.H4("Generation of conformers may take longer, especially with numerous compounds.",
                            className='run-select-info-text', style={'margin-left': '20px'}),
                    html.Div(style={'margin-bottom': '10px'}, children=[
                        dcc.Loading(
                            id='loading-csv',
                            type='circle',
                            children=[
                            html.Button('PROPERTIES (.csv)', id='generate-csv', n_clicks=0, style={
                                'width': '400px'
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
                    ])
                ],
                         style={
                             'width': '420px'
                         })
            ])
        ]),
        dcc.Store(id='conformers_generated'),
        dcc.Store(id='products'),
        dcc.Store(id='summary-store'),
        dcc.Store(id='structures-store'),
        dcc.Store(id='table-store', storage_type='local'),
        dcc.Store(id='fig-store'),
        html.H1('GENERATED PUR FRAGMENTS', className='highlighted-center-text'),
        dcc.Tabs(id="tabs", value='tab-structures', children=[
            dcc.Tab(label='PUR structures', value='tab-structures'),
            dcc.Tab(label='Calculated properties', value='tab-table'),
            dcc.Tab(label='Properties histograms', value='tab-histograms')
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

    table = dash_table.DataTable(
        compounds_properties_df.to_dict('records'),
        style_data={'textAlign': 'left'},
        style_header={'textAlign': 'left'}
    )

    return summary, structures_imgs, table, fig, compounds_properties_df.to_dict('records')


@callback(
    Output('summary-store', 'data'),
    Output('structures-store', 'data'),
    Output('table-store', 'data'),
    Output('fig-store', 'data'),
    Output('summary-output', 'children'),
    #Output('conformers-generated', 'data'),
    Input('stored-substrates', 'data'),
    Input('stored-size', 'data'),
    Input('stored-capping', 'data')
)
def initialize_data(stored_substrates, stored_size, stored_capping):
    summary, structures_imgs, table, fig, compounds_data = prepare_data(stored_substrates, stored_size, stored_capping)
    fig_data = fig.to_plotly_json()
    return summary, structures_imgs, compounds_data, fig_data, summary


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
        table = dash_table.DataTable(
            table_data,
            style_data={'textAlign': 'left'},
            style_header={'textAlign': 'left'}
        )
        tab_output = html.Div(children=[
            html.Center(html.H4('''Calculated PUR fragments properties:
                molecular weight, heavy atom count, number of rotatable bonds, 
                presence of ester and ether bonds, count of aromatic atoms, aromatic proportion 
                (ratio of aromatic atoms to heavy atoms), Crippen-Wildman partition coefficient 
                (cLogP), topological polar surface area 
                (TPSA) and Crippen-Wildman molar refraction (MR).''',
                                className='results-properties-description')),
            table,
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
    State('table-store', 'data'),
    prevent_initial_call=True
)
def download_csv(n_clicks, table_data):
    if n_clicks and table_data:  # Ensure table_data is passed
        df = pd.DataFrame(table_data)
        return dcc.send_data_frame(df.to_csv, "properties.csv", index=False)


@callback(
    Output('download-2d', 'data'),
    Input('generate-2d', 'n_clicks'),
    State('table-store', 'data'),
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
    Input('table-store', 'data'),
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
    Input('table-store', 'data'),
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