import dash
from dash import html, dcc, callback
from dash.dependencies import Input, Output, State

dash.register_page(__name__, path='/')

external_stylesheets = ['assets/style.css']

# Define layout for the home page
layout = html.Div(id = 'home-page',
    className='home-page-style',
    children = [html.Center(id = 'logo', style = {'alignItems': 'center', 'height': 'auto'},
    children = [html.A(html.Img(src='assets/pur-gen.png', className = 'homepage-logo'),href='/'),
                html.Div(style={'display':'flex', 'justify-content': 'center', 'margin-top':'50px', 'margin-bottom':'30px'},
                         children=[
                dcc.Link(html.Button('HOW TO USE', id='how-to-use-button', n_clicks=0), href='/how-to-use'),
                dcc.Link(html.Button('RUN PUR-GEN', id='run-pur-gen-button', n_clicks=0), href='/run')
                         ]),
                
                html.H3('''PUR-GEN is a chemoinformatics online tool, which generates single structures or libraries of polyurethane (PUR) fragments.
                        Generated structures can be further used in computational analyses such as molecular docking, see: 
                        ''',
                className = 'homepage-text-main'),
                html.A("PUR-GEN: a tool for polyurethane fragments generation and its applicability for computational biodegradation studies, Szleper K., Raczyńska A., Góra A., 2024", 
                       href='http://www.doi.pl/',className='homepage-publication-link',style={'maxWidth': '80%', 'display': 'inline-block','whiteSpace': 'normal','lineHeight': '1.5'}),
                
                html.Img(src='assets/PUR.png',style={'width': '100%','opacity':'0.3','margin-top': '50px',}),
                html.H3("Contact Information", className = 'contact-info'),
                html.H3("email: k.szleper@tunnelinggroup.pl", className = 'email-info'),
                html.H3("VISIT OUR WEBPAGE!", className = 'tg-info'),
                html.A("Tunneling Group", href='http://www.tunnelinggroup.pl/', 
                       title = 'http://www.tunnelinggroup.pl/', className = 'tg-link'),
                     html.Br()
                ])
])