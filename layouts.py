from dash import html, dcc
import dash_daq as daq
import utils

def create_checkbox_list(options, all_options, table_title, table_id, checkall_id, checklist_id):
    return html.Div(
        style={},
        id = table_id,
        children = [html.H3(table_title, className='highlighted-left-text'),
                    dcc.Checklist(id = checkall_id,
                                  options = [{'label': html.H4('select all',className='substrate-checklist-text'), 
                                              'value':all_options}], 
                                  value = [],style={'margin-bottom':'10px'}),
            
                    dcc.Checklist(id = checklist_id,
                                  options = [{'label': html.Div([html.H4([option['label']],
                                                                         className='substrate-checklist-text'),
                                                                 html.Img(src='data:image/jpeg;base64,'+ utils.smiles_to_image(option['smiles']),
                                                                          style={'height': '150px','width':'auto', 'margin': '0'}),
                                                                 ]),
                                              'value': option['smiles']
                                              } for option in options],
                                  value=[],)
                    ])

def create_switch_with_label(label_text, switch_id,image_source):
    return html.Div([
        daq.BooleanSwitch(
            id=switch_id,
            on=False
        ),
        html.Div([html.H4(
            label_text,
            className = 'switch-label'
        ),
        html.Img(src=image_source, style={'height': '50px','width': 'auto', 'margin-left':'15px'})])
    ], style={'display': 'flex', 'align-items': 'left'})
    
def create_upload_component():
    return html.Div([
        dcc.Upload(
            id='upload-substrates',
            children=[
                html.Div('Drag and Drop', style={'margin-top':'10px','font-weight': 'bold', 'font-size': '16px', 'font-weight': '600', 'line-height': '25px', 'letter-spacing': '.1rem', 'text-transform': 'uppercase', 'text-decoration': 'none', 'font-weight': 'normal', 'white-space': 'nowrap'}),
                html.Div('or', style={'font-weight': 'bold', 'font-size': '16px', 'font-weight': '600', 'line-height': '25px', 'letter-spacing': '.1rem', 'text-decoration': 'none', 'font-weight': 'normal', 'white-space': 'nowrap'}),
                html.Div('Select Input File', style={'font-weight': 'bold', 'font-size': '16px', 'font-weight': '600', 'line-height': '25px', 'letter-spacing': '.1rem', 'text-transform': 'uppercase', 'text-decoration': 'none', 'font-weight': 'normal', 'white-space': 'nowrap'}),
                ],
            className='upload-component',
            multiple=False
        ),
        html.H5(id='successful-upload', 
                children=[],className='successful-upload'),
        html.A("sample_input.txt", href="static/sample_input.txt",className='successful-upload')
    ])

def create_select_size_component():
    return html.Div([
        html.H3("SELECT SIZE", className='run-select-text'),
        html.H4(children=[],className='run-select-info-text', id='size-info'),
        dcc.RadioItems(
            id='select-size',
            options=[
                {'label': html.Label(['2 units', html.Img(src='assets/size-2.png', style={'height': '50px','width': 'auto', 'margin-left':'15px', 'margin-bottom':'-10px'})]), 'value': '2'},
                {'label': html.Label(['3 units', html.Img(src='assets/size-3.png', style={'height': '50px','width': 'auto', 'margin-left':'15px', 'margin-bottom':'-10px'})]), 'value': '3'},
                {'label': html.Label(['4 units', html.Img(src='assets/size-4.png', style={'height': '50px','width': 'auto', 'margin-left':'15px', 'margin-bottom':'-10px'})]), 'value': '4'},
            ],
            value='2',  # Default selected value
            labelStyle={
                'display': 'block',
                'margin-top': '-5px',
                'margin-bottom': '10px',
                'margin-left': '5px',
                'color': 'gray',
                'font-size': '15px',
                'font-weight': '600',
                'line-height': '25px',
                'letter-spacing': '.1rem',
                'text-decoration': 'none',
                'font-weight': 'normal',
                'white-space': 'nowrap'
            },  
        ),
    ])

def create_capping_group_component():
    return html.Div([
        html.H3("SELECT CAPPING GROUP", className='run-select-text'),
        dcc.Dropdown(
            ['-NH2', '-CH3', '-N=C=O', '-NC(=O)OH'],
            placeholder="Select isocyanate capping group",
            id='capping-group'
        )])

def create_download_panel():
    return html.Div(id = 'left-panel-download', 
                                  style = {'display':'none'},
                                  children = [html.Div([
                                      html.H5("Save all generated PU fragments in SMILES (PU.txt).", style={'color':'gray', 'margin-bottom': '-3px', 'margin-left':'5px', 'textAlign': 'center', 'font-weight': 'normal'}), 
                                      html.Button("GENERATE SMILES", id='generate-smiles', n_clicks=0, style={'margin':'5px'} ),
                
                html.Div([
                    dcc.Loading(id='loading-smiles',
                                style ={'margin-left': '15px'},
                                type='dot',
                                children=[html.Div(id="download-smiles", style={'textAlign': 'center', 'margin':'5px','opacity': '0.6'})]
                    )
                ]),
                html.H5("Save generated PU fragments as 2D .mol files.", style={'color':'gray', 'margin-bottom': '-3px', 'margin-left':'5px', 'textAlign': 'center', 'font-weight': 'normal'}), 
                html.Button("GENERATE 2D STRUCTURES (.mol)", id='generate-mol', n_clicks=0,style={'margin':'5px'}),
                html.Div([
                    dcc.Loading(id='loading-mol',
                                type='dot',
                                children=[html.Div(id="download-mol", style={'textAlign': 'center','margin':'5px','opacity': '0.6'})]
                    )
                ]),
                html.H5("Save generated PU fragments as 3D .mol2 files.", style={'color':'gray', 'margin-bottom': '-3px', 'margin-left':'5px', 'textAlign': 'center', 'font-weight': 'normal'}),
                html.Button("GENERATE 3D STRUCTURES (.mol2)", id='generate-mol2', n_clicks=0,style={'margin':'5px'} ),
                html.Div([
                    dcc.Loading(id='loading-mol2',
                                type='dot',
                                children=[html.Div(id="download-mol2", style={'textAlign': 'center', 'margin':'5px','opacity': '0.6'})]
                    )
                ]),
                html.H5("Generate 20 conformers for 3D structures of PU fragments.", style={'color':'gray', 'margin-bottom': '-3px', 'margin-left':'5px', 'textAlign': 'left', 'font-weight': 'normal'}),
                html.Div("This action can take a while depending on the number of products.", style={'color':'gray', 'margin-bottom': '-3px', 'margin-left':'5px', 'textAlign': 'left', 'font-weight': 'bold', 'font-size':'13px'}),
                html.Button("GENERATE 3D STRUCTURES WITH CONFORMERS (.mol2)", id='generate-conformers', n_clicks=0,style={'margin':'5px'}),
                html.Div([
                    dcc.Loading(id='loading-conformers',
                                type='dot',
                                children=[html.Div(id="download-conformers", style={'textAlign': 'center', 'margin':'5px', 'opacity': '0.6'})]
                    )
                ]),
                html.H5("Save generated PU fragments as images.", style={'color':'gray', 'margin-bottom': '-3px', 'margin-left':'5px', 'textAlign': 'center', 'font-weight': 'normal'}),
                html.Button("GENERATE IMAGES (.png)", id='generate-images', n_clicks=0,style={'margin':'5px'} ),
                html.Div([
                    dcc.Loading(id='loading-images',
                                type='dot',
                                children=[html.Div(id="download-images", style={'textAlign': 'center', 'margin':'5px','opacity': '0.6'})]
                    )
                ])
                ], style={'display': 'flex', 'flex-direction': 'column', 'align-items':'flex-start', 'textAlign': 'left'})
            ])

def create_footer():
    return html.Div(id = 'left-panel-footer', children = [
            html.Div(children = [html.Div(className='circle', style = {'background-color': '#FAAAAA','margin-right':'20px'}),
                                html.Div(className='circle', style = {'background-color': '#ABABAB',
                                                                        'margin-right':'20px'}),
                                html.Div(className='circle', style = {'background-color': '#9f74f2'})],
                                                style = {'display':'flex', 'justify-content': 'center', 'margin-top':'15px', 'margin-bottom':'15px'}),
            ])