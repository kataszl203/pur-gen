from dash import html, dcc
import dash_daq as daq
import utils



def create_checkbox_list(options, table_title, table_id, checkall_id, checklist_id):
    return html.Div(
        style={'flex': '1', 
               'padding': '10px', 
               'display':'none'},
        id = table_id,
        children = [html.H3(table_title, style={'text-align': 'left'}),
                    dcc.Checklist(id = checkall_id,
                                  options = [{'label': 'select all', 'value':'all'}], 
                                  value = [],
                                  style={'margin-bottom':'10px',
                                         'font-weight':'lighter'}),
            
                    dcc.Checklist(id = checklist_id,
                                  options = [{'label': html.Div([html.H4([option['label']],
                                                                         style={'display': 'block',
                                                                                'font-weight': 'normal',
                                                                                'margin-left': '25px',
                                                                                'margin-top':'-20px'}),
                                                                 html.Img(src='data:image/jpeg;base64,'+ utils.smiles_to_image(option['smiles']),
                                                                          style={'height': '200px','width':'auto', 'margin': '0'}),
                                                                 ]),
                                              'value': option['smiles']
                                              } for option in options],
                                  value=[],)
                    ])

def create_right_panel():
    return html.Div(children = [html.Img(id = 'right-panel-header', 
                                src='assets/PUR.png', 
                                style={}),
                                html.Div(id = 'main-page',
                                children = [
                                html.H2("Generate PUR oligomers for computational analyses",
                                        style={'font-weight': '200',
                                                'font-size': '25px',
                                                'letter-spacing': '.2rem',
                                                'margin-top': '10px',
                                                'margin-bottom': '10px',
                                                'color': '#737373',
                                                'textAlign': 'center',
                                                'opacity':'0.8',
                                                }),
                                html.H2("HOW IT WORKS?",
                                            style={'font-weight': '200',
                                                'font-size': '30px',
                                                'letter-spacing': '.1rem',
                                                'margin-top': '30px',
                                                'margin-bottom': '50px',
                                                'color': '#737373',
                                                'textAlign': 'center',
                                                'text-shadow': '1.2px 1.2px #919191',
                                                'opacity':'0.8',
                                                }),
                                html.Div(children = [html.Div(className='circle', style = {'background-color': '#FAAAAA'})],
                                style = {'display':'flex', 'justify-content': 'center'}),
                                html.H2("SELECT SUBSTRATES",
                                            style={'font-weight': '500',
                                                'font-size': '18px',
                                                'letter-spacing': '.1rem',
                                                'margin-top': '50px',
                                                'margin-bottom': '30px',
                                                'color': '#737373',
                                                'textAlign': 'center'
                                                }),
                                html.Div([html.Img(src='assets/substrates.png',
                                                    style={'max-width': '80%'})],
                                            style = {'display':'flex', 'justify-content': 'center', 'margin-bottom': '50px'}),
                                html.Div(children = [html.Div(className='circle', style = {'background-color': '#ABABAB'})],
                                style = {'display':'flex', 'justify-content': 'center'}),
                                html.H2("SELECT SIZE AND CAPPING GROUPS",
                                            style={'font-weight': '500',
                                                'font-size': '18px',
                                                'letter-spacing': '.1rem',
                                                'margin-top': '50px',
                                                'margin-bottom': '10px',
                                                'color': '#737373',
                                                'textAlign': 'center',
                                                }),
                                html.Div([html.Img(src='assets/sizes.png',
                                                    style={'max-width': '80%'})],
                                            style = {'display':'flex', 'justify-content': 'center', 'margin-bottom': '30px'}),
                                
                                html.Div(children = [html.Div(className='circle', style = {'background-color': '#9f74f2'})],
                                style = {'display':'flex', 'justify-content': 'center'}),
                                html.H2("DOWNLOAD STRUCTURES",
                                            style={'font-weight': '500',
                                                'font-size': '18px',
                                                'letter-spacing': '.1rem',
                                                'margin-top': '50px',
                                                'margin-bottom': '10px',
                                                'color': '#737373',
                                                'textAlign': 'center',
                                                }),
                                html.Div([html.Img(src='assets/downloads.png',
                                                    style={'max-width': '60%'})],
                                            style = {'display':'flex', 'justify-content': 'center', 'margin-bottom': '50px'})
                                ],
                                style = {}),
                                html.Div(id = 'main-after-reaction',
                                            children = [
                                                html.Div(children = [html.Div(className='circle', style = {'background-color': '#FAAAAA',
                                                                                                            'margin-right':'40px'}),
                                                                    html.Div(className='circle', style = {'background-color': '#ABABAB',
                                                                                                            'margin-right':'40px'}),
                                                                    html.Div(className='circle', style = {'background-color': '#9f74f2'})],
                                                style = {'display':'flex', 'justify-content': 'center', 'margin-top':'30px', 'margin-bottom':'30px'}),
                                                ],
                                            style = {})
                                ],
                    style = {'display': 'block'})

def create_switch_with_label(label_text, switch_id):
    return html.Div([
        daq.BooleanSwitch(
            id=switch_id,
            on=False
        ),
        html.H4(
            label_text,
            style ={'font-weight': 'normal',
                    'margin-top': '0px', 
                    'margin-bottom': '10px', 
                    'margin-left': '10px',
                    'color': 'gray',
                    'font-size': '14px',
                    'font-weight': '600',
                    'line-height': '25px',
                    'letter-spacing': '.1rem',
                    'text-decoration': 'none',
                    'font-weight': 'normal',
                    'white-space': 'nowrap'
                    }
        ),
    ], style={'display': 'flex', 'align-items': 'left'})
    
def create_upload_component():
    return html.Div([
        dcc.Upload(
            id='upload-substrates',
            children=[
                html.Div('Drag and Drop', style={'font-weight': 'bold', 'font-size': '14px', 'font-weight': '600', 'line-height': '25px', 'letter-spacing': '.1rem', 'text-transform': 'uppercase', 'text-decoration': 'none', 'font-weight': 'normal', 'white-space': 'nowrap'}),
                html.Div('or', style={'font-weight': 'bold', 'font-size': '14px', 'font-weight': '600', 'line-height': '25px', 'letter-spacing': '.1rem', 'text-decoration': 'none', 'font-weight': 'normal', 'white-space': 'nowrap'}),
                html.Div('Select Input File', style={'font-weight': 'bold', 'font-size': '14px', 'font-weight': '600', 'line-height': '25px', 'letter-spacing': '.1rem', 'text-transform': 'uppercase', 'text-decoration': 'none', 'font-weight': 'normal', 'white-space': 'nowrap'})
            ],
            style={
                'width': '100%',
                'height': '80px',
                'lineHeight': '80px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '0px',
                'cursor': 'pointer',
            },
            multiple=False
        ),
        html.H5(id='successful-upload', children=[], style={'color': 'gray', 'margin-top': '5px', 'textAlign': 'center', 'font-weight': 'normal'}),
        dcc.Store(id='uploaded-data'),
    ])

def create_select_size_component():
    return html.Div([
        html.H3("SELECT SIZE", style={'font-weight': 'normal', 'margin-top': '0px', 'margin-bottom': '8px'}),
        dcc.RadioItems(
            id='select-size',
            options=[
                {'label': '2 units', 'value': '2'},
                {'label': '3 units', 'value': '3'},
                {'label': '4 units', 'value': '4'},
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
        html.H3("SELECT CAPPING GROUP", style={'font-weight': 'normal', 'margin-top': '20px', 'margin-bottom': '5px'}),
        dcc.Dropdown(
            ['-NH2', '-CH3', '-N=C=O', '-NC(=O)OH'],
            placeholder="Select isocyanate capping group",
            id='capping-group'
        ),
        html.Div([html.Button(
            "RUN",
            id='make-oligomers-button',
            n_clicks=0,
            style={'margin-top': '30px', 'textAlign': 'center', 'background-color': '#ba9ef0'}
        )], style = {'display':'flex', 'justify-content': 'center'}),
    ])

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
            html.Div(children = [html.Div(className='circle', style = {'background-color': '#FAAAAA',
                                                                                                            'margin-right':'20px'}),
                                                                    html.Div(className='circle', style = {'background-color': '#ABABAB',
                                                                                                            'margin-right':'20px'}),
                                                                    html.Div(className='circle', style = {'background-color': '#9f74f2'})],
                                                style = {'display':'flex', 'justify-content': 'center', 'margin-top':'15px', 'margin-bottom':'15px'}),
                                                
            
            html.H3("See the related publication", style={'color': '5b5d74',
                                                'font-size': '15px',
                                                'font-weight': '600',
                                                'line-height': '15px',
                                                'letter-spacing': '.1rem',
                                                'text-transform': 'uppercase',
                                                'text-decoration': 'none',
                                                'font-weight': 'bold',
                                                'white-space': 'nowrap',
                                                'textAlign': 'center',
                                                'margin-top':'30px',
                                                'margin-bottom':'15px',
                                                'opacity': '0.6'}),
            html.A("Title of the publication, Authors, 2023", href='http://www.doi.pl/', style={'color': '5b5d74',
                                                'font-size': '14px',
                                                'font-weight': '600',
                                                'line-height': '14px',
                                                'letter-spacing': '.1rem',
                                                'text-decoration': 'none',
                                                'font-weight': 'normal',
                                                'white-space': 'nowrap',
                                                'display': 'flex',  # Set display to flex
                                                'justify-content': 'center',  # Center horizontally
                                                'align-items': 'center',  # Center vertically
                                                'margin-bottom': '40px'
                                                }),
             
            html.A("GitHub repository of the project", href='https://github.com/kataszl203', style={'color': '5b5d74',
                                                'font-size': '14px',
                                                'font-weight': '600',
                                                'line-height': '14px',
                                                'letter-spacing': '.1rem',
                                                'text-decoration': 'none',
                                                'font-weight': 'bold',
                                                'white-space': 'nowrap',
                                                'display': 'flex',  # Set display to flex
                                                'justify-content': 'center',  # Center horizontally
                                                'align-items': 'center',  # Center vertically
                                                'margin-bottom': '40px',
                                                'opacity': '0.6'
                                                }),
            html.H3("Contact Information", style={'color': '5b5d74',
                                                'font-size': '15px',
                                                'font-weight': '600',
                                                'line-height': '15px',
                                                'letter-spacing': '.1rem',
                                                'text-transform': 'uppercase',
                                                'text-decoration': 'none',
                                                'font-weight': 'bold',
                                                'white-space': 'nowrap',
                                                'textAlign': 'center',
                                                'margin-bottom':'-5px',
                                                'opacity': '0.6'}),
            html.H3("email: k.szleper@tunnelinggroup.pl", style={'color': '5b5d74',
                                                'font-size': '14px',
                                                'font-weight': '600',
                                                'line-height': '14px',
                                                'letter-spacing': '.1rem',
                                                'text-decoration': 'none',
                                                'font-weight': 'normal',
                                                'white-space': 'nowrap',
                                                'textAlign': 'center',
                                                }),
            html.H3("VISIT OUR WEBPAGE!", style={'color': '5b5d74',
                                                'font-size': '14px',
                                                'font-weight': '600',
                                                'line-height': '14px',
                                                'letter-spacing': '.1rem',
                                                'text-decoration': 'none',
                                                'font-weight': 'bold',
                                                'white-space': 'nowrap',
                                                'textAlign': 'center',
                                                'margin-top': '30px',
                                                'margin-bottom':'15px',
                                                'opacity': '0.6'
                                                }),
            html.A("Tunneling Group", href='http://www.tunnelinggroup.pl/', title = 'http://www.tunnelinggroup.pl/', style={'color': '5b5d74',
                                                'font-size': '18px',
                                                'font-weight': '600',
                                                'line-height': '18px',
                                                'letter-spacing': '.1rem',
                                                'text-decoration': 'none',
                                                'font-weight': 'normal',
                                                'white-space': 'nowrap',
                                                'display': 'flex',  # Set display to flex
                                                'justify-content': 'center',  # Center horizontally
                                                'align-items': 'center',  # Center vertically
                                                'margin-bottom': '20px'
                                                })
            ])