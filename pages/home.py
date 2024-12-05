import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, 
                   path='/',
                   title='PUR-GEN',
                   name='PUR-GEN',
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
# Define layout for the home page
layout = html.Div(
    className='home-page-style',
    children = [navbar, html.Center(style = {'alignItems': 'center', 'margin-top': '60px'},
    children = [html.A(html.Img(src='assets/pur-gen_tg_full_logo.png', className = 'homepage-logo'),href='/'),
                html.Div(className='header-buttons',children=[
                #dcc.Link(html.Button('HOW TO USE'), href='/how-to-use'),
                # dcc.Link(html.Button('RUN PUR-GEN'), href='/run')
                ]),

                html.H3('''PUR-GEN is a chemoinformatics online tool, 
                        which generates single structures or libraries 
                        of polyurethane (PUR) fragments.
                        ''',
                className = 'homepage-text-main'),

                html.H3('''Generated structures can be further used in 
                        computational analyses such as molecular docking, see: 
                        ''',
                className = 'homepage-text-main'),
                
                html.A('''PUR-GEN: A Web Server for Automated Generation of Polyurethane Fragment Libraries, 
                       K. Szleper, M. Cebula, O. Kovalenko, A. Góra, A. Raczyńska, 2024 (to be published)''', 
                       className='homepage-publication-link'),
                     #   href='http://www.doi.pl/',className='homepage-publication-link'), #Link of publication to be added
                html.Img(src='assets/graphical-abstract-v2.png',#'assets/abstract.png',
                         style={'width': '40%','margin-top': '10px', 'margin-bottom':'20px'}),
                         
                html.H3("Contact Information", className = 'contact-info'),
                html.H3("Katarzyna Szleper", className = 'email-info'),
                html.H3("email: k.szleper@tunnelinggroup.pl  katarzyna.szleper@polsl.pl", className = 'email-info'),
                html.H3("VISIT OUR WEBPAGE:", className = 'tg-info'),
                html.A("Tunneling Group", href='http://www.tunnelinggroup.pl/', 
                       title = 'http://www.tunnelinggroup.pl/', className = 'tg-link', target='_blank'),
                     html.Br()
                ])
])