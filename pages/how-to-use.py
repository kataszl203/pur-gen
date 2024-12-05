import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, 
                   path='/how-to-use',
                   title='how to use PUR-GEN',
                   name='how to use PUR-GEN',
                   image='assets/logo.png')

buttons = dbc.Row(
    [
        dbc.Col(
            dbc.Button(
                "RUN PUR-GEN",
                color="primary",
                href="/run",
                className='button',  # Single 'button' class for CSS
                n_clicks=0
            ),
            width="auto",
        ),
        dbc.Col(
            dbc.Button(
                "HOME",
                href="/",
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

# Define layout for the "How to Use" page
layout = html.Center(style = {'display': 'block','alignItems': 'center', 'margin-top': '60px'},
    children = [navbar,
        html.Center(className='how-to-use-page-header',children = [
            html.A(html.Img(src='assets/pur-gen_tg_full_logo.png', className = 'homepage-logo'),href='/',id='top'),
                    html.Div(className='header-buttons',children=[
                        #dcc.Link(html.Button('HOME PAGE'), href='/'),
                        # dcc.Link(html.Button('RUN PUR-GEN'), href='/run')
                        ]),
                    ]),

    html.H2("HOW IT WORKS?", className = 'highlighted-center-text'),

    html.H3('''PUR-GEN is designed for the automated generation of PUR fragments libraries.''', 
            className='center-text'),
    html.H3('''Follow the steps to obtain PUR structures:''', 
            className='center-text'),
    html.Div(children = [html.Div(className='circle-pink')], className='how-to-use-circle'),
    
    html.H2("1. SELECT OR UPLOAD SUBSTRATES",className='highlighted-center-smaller-text'),
    
    html.Div([html.Img(src='assets/substrates-v2.png',
                       style={'max-width': '40%'})],
                       className='how-to-use-image'),

    html.H3('''PUR fragments can be generated from diverse groups of both main 
            substrates used for PUR synthesis: isocyanates and alcohols. 
            PUR-GEN provides a collection of isocyanate structures that are often used in industrial applications and
            a range of alcohols, which enables introduction of ester or ether 
            bonds into the resulting PUR fragments, closely mimicking the composition of commercially utilised polyether and polyester polyols. 
            ''', 
            className='center-text'),

    html.Img(src='assets/select-substrates-v2.png', className='how-to-use-screenshot'),

    html.H3('''To generate other desired motifs, one can also type other 
            substrate structures in SMILES format. To facilitate SMILES generation for other input structures, user can use linked "SMILES GENERATOR".''', 
            className='center-text'),
    html.H3('''Input text should be prepared as the following example:''', 
            className='center-text'),

    html.Img(src='assets/test-input-v2.png', className='how-to-use-screenshot'),

    html.H3('''After selecting isocyanates and alcohols from the list and loading additional input compounds, all substrates are summarised in a table:''', 
            className='center-text'),

    html.Img(src='assets/selected-substrates.png', className='how-to-use-screenshot'),

    html.H3('''To generate PUR fragments at least one isocyanate and one alcohol should be selected.''', 
            className='center-text'),

    html.Div(children = [html.Div(className='circle-grey')],className='how-to-use-circle'),

    html.H2("2. SELECT PARAMETERS: SIZE AND CAPPING GROUPS",className='highlighted-center-smaller-text'),
    
    html.Div([html.Img(src='assets/fragment-size-v2.png',
                        style={'max-width': '50%'})],
                        className='how-to-use-image'),
    html.H3(''' Users can specify the desired length of the PUR fragments they aim to generate. 
            The minimum "2 units" fragments contain one molecule of each comonomer connected by a urethane bond. 
            Then, "3 units" consist of three structural units: two molecules of one comonomer and one of the other. 
            The structural unit in the middle must have two functional groups (-NCO or -OH). 
            The longest one, "4 units" consists of four structural units; two molecules of each comonomer. 
            The synthesis of such a fragment requires the use of structural units with two functional groups each. ''', 
            className='center-text'),
    html.Div([html.Img(src='assets/isocyanate-replacement.png',
                        style={'max-width': '20%'})],
                        className='how-to-use-image'),

    html.H3('''Depending on the number of functional groups in the structural units employed, 
            the resulting PUR fragments may contain reactive isocyanate moieties (-N=C=O). 
            The user has the option of replacing these groups with another neutral capping group, 
            one of amine (-NH2), methyl (-CH3) or carbamate (-NC(=O)OH). 
            This feature proves particularly advantageous for applications such as molecular docking, 
            as it allows to reduce the partial charge on atoms resulting from the discontinuity of the modelled polymer chain. ''', 
            className='center-text'), 

    html.Img(src='assets/select-size-v2.png', className='how-to-use-screenshot'),    
    html.H3('''These are the only input settings needed to run the program. Click "CALCULATE PRODUCTS" to generate PUR fragments.''', 
            className='center-text'),                
    
    html.Div(children = [html.Div(className='circle-purple')],className='how-to-use-circle'),
    
    html.H2("3. RESULTS",className='highlighted-center-smaller-text'),

    html.Div([html.Img(src='assets/output.png',
                        style={'max-width': '60%'})],
                        className='how-to-use-image'),

    html.H3('''PUR-GEN generates a summary and short analysis of obtained compounds. 
            In a tab "PUR structures" are presented structures of geneated PUR fragments.
            Tab "Calculated properties" contains information about 
            molecular weight, heavy atom count, number of rotatable bonds, 
            presence of ester and ether bonds, count of aromatic atoms, aromatic proportion 
            (ratio of aromatic atoms to heavy atoms), Crippen-Wildman partition coefficient 
            (cLogP), Crippen-Wildman molar refraction (MR) and topological polar surface area 
            (TPSA).
            Tab "Properties histograms" shows the calculated data on plots.  
            ''', 
            className='center-text'),

    html.Img(src='assets/results-v2.png', className='how-to-use-screenshot-margin'),

    html.H3('''After clicking "DOWNLOAD GENERATED DATA" user can select PUR fragments that will be downloaded.
            Compounds can be downloaded as: 2D structures (.mol file format) and 3D structures (.mol2 file format).
            It is also possible to generate up to 20 conformers, however, larger or more complex compounds from PUR-GEN may produce fewer conformers, sometimes only one structure.
            Calculated properties can be also downloaded as a table in .csv file format.''', 
            className='center-text'),
    
    html.Img(src='assets/download.png', className='how-to-use-screenshot-margin'),

    html.Div(dcc.Link(html.Button("back to top of the page"), href='#top')),

    html.Br(),
    html.H3("Contact Information", className = 'contact-info'),
    html.H3("Katarzyna Szleper", className = 'email-info'),
    html.H3("email: k.szleper@tunnelinggroup.pl  katarzyna.szleper@polsl.pl", className = 'email-info'),
    html.H3("VISIT OUR WEBPAGE!", className = 'tg-info'),
    html.A("Tunneling Group", href='http://www.tunnelinggroup.pl/', 
                       title = 'http://www.tunnelinggroup.pl/', className = 'tg-link', target='_blank'),
    html.Br()
    ])