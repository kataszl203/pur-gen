import dash
from dash import html, dcc, callback, callback_context, no_update
from dash.dependencies import Input, Output, State
import layouts
import callbacks
from dash.exceptions import PreventUpdate


dash.register_page(__name__, path='/run')

external_stylesheets = ['assets/style.css']

# Read the compounds
isocyanate_list = [{'label' : i.split(";")[0], 'smiles' : i.split(";")[1]} for i in open("data/isocyanates.txt", "r").read().splitlines()]
hydroxyl_list = [{'label' : i.split(";")[0], 'smiles' : i.split(";")[1]} for i in open("data/poliols.txt", "r").read().splitlines()]
isocyanate_all = [item['smiles'] for item in isocyanate_list]
hydroxyl_all = [item['smiles'] for item in hydroxyl_list]

layout = html.Div(style={'display': 'flex'},
    children=[html.Div(id = 'left-panel-content',className='run-left-panel-layout',
                       children = [
    html.Div(id = 'left-panel-header',
            children = [html.A(html.Img(src='assets/pur-gen.png', 
                                    style={'max-width': '85%', 
                                           'height': 'auto'}), 
                                    href='/'),]),
    html.Div(id = 'left-panel-before-reaction',
            children = [html.H3("SELECT SUBSTRATES",className='run-select-text'),
                        html.H4("Choose at least one isocyanate and one hydroxyl compound.",
                                className='run-select-info-text'),
                        layouts.create_switch_with_label('show isocyanates','switch-isocyanate'),
                        layouts.create_switch_with_label('show hydroxyl compounds','switch-hydroxyl'),
                        layouts.create_upload_component(),
                        dcc.Store(id='store-substrates'),
                        layouts.create_select_size_component(),
                        layouts.create_capping_group_component(),
                        html.Div([dcc.Link(html.Button("RUN",
                            className='button button',
                            n_clicks=0),id='make-oligomers-button',href='')], 
                            style = {'display':'flex', 
                                     'justify-content': 'center',
                                     'margin-top':'50px',
                                     'margin-bottom':'50px'})]),
    dcc.Store(id='store-reaction')]),
              html.Div([
                  html.Div(id = 'right-panel-content',
                           children = [layouts.create_checkbox_list(isocyanate_list, isocyanate_all, "Select isocyanates: ", 'isocyanate-list', 'select-all-isocyanate', 'isocyanate-list-checkbox'),
                                       layouts.create_checkbox_list(hydroxyl_list, hydroxyl_all, "Select hydroxyl compounds:", 'hydroxyl-list', 'select-all-hydroxyl', 'hydroxyl-list-checkbox'),
                                       ],
                           style={'display':'flex'})],
                       style={'flex': '2'}),
              ])

# Define callback to show substrates lists
@callback(Output('hydroxyl-list', 'style'),
        Output('isocyanate-list', 'style'),
        Input('switch-hydroxyl','on'),
        Input('switch-isocyanate','on'))
def show_substrates(hydroxyl_clicks,isocyanate_clicks):
    if isocyanate_clicks and hydroxyl_clicks:
        hydroxyl_list_style = {'display':'block','flex': '1', 'padding': '10px'}
        isocyanate_list_style = {'display':'block','flex': '1', 'padding': '10px'}
    
    elif isocyanate_clicks:       
        hydroxyl_list_style = {'display':'none'}
        isocyanate_list_style = {'display':'block','flex': '1', 'padding': '10px'}

    elif hydroxyl_clicks:        
        hydroxyl_list_style = {'display':'block','flex': '1', 'padding': '10px'}
        isocyanate_list_style = {'display':'none'}
    
    else:
        hydroxyl_list_style = {'display':'none'}
        isocyanate_list_style = {'display':'none'}

    return hydroxyl_list_style, isocyanate_list_style

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

# Define callback to validate uploaded input 
# and store uploaded substrates together with selected substrates
@callback(Output('successful-upload', 'children'),
          Output('stored-substrates', 'data'),
          Output('make-oligomers-button', 'href'),
        Input('upload-substrates', 'contents'),
        State('upload-substrates', 'filename'),
        Input('isocyanate-list-checkbox', 'value'),
        Input('hydroxyl-list-checkbox', 'value'))
def validate_input(contents, filename, 
                   isocyanate_checkbox_value, hydroxyl_checkbox_value, 
                   ):
    #Validate input and read compounds
    valid_file, uploaded_substrates = callbacks.validate_input_file(contents, filename)
    
    #Read selected substrates
    smiles = isocyanate_checkbox_value + hydroxyl_checkbox_value
    
    #Combinde uploaded and selected substrates
    for substrate in uploaded_substrates:
        if substrate not in smiles:
            smiles.append(substrate)
    if not smiles:
        return no_update

    if smiles:
        return valid_file, smiles, '/results'


# Define callback to store size and capping groups
@callback(Output('stored-size', 'data'),
          Output('stored-capping', 'data'),
          Input('select-size', 'value'),
          Input('capping-group', 'value') 
          )

def store_size_and_capping(size_value, capping_value):
    return size_value, capping_value