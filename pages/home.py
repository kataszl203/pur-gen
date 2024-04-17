import dash
from dash import html, dcc

dash.register_page(__name__, path='/')

# Define layout for the home page
layout = html.Div(
    className='home-page-style',
    children = [html.Center(style = {'alignItems': 'center'},
    children = [html.A(html.Img(src='assets/pur-gen.png', className = 'homepage-logo'),href='/'),
                html.Div(className='header-buttons',children=[
                dcc.Link(html.Button('HOW TO USE'), href='/how-to-use'),
                dcc.Link(html.Button('RUN PUR-GEN'), href='/run')]),

                html.H3('''PUR-GEN is a chemoinformatics online tool, 
                        which generates single structures or libraries 
                        of polyurethane (PUR) fragments.
                        Generated structures can be further used in 
                        computational analyses such as molecular docking, see: 
                        ''',
                className = 'homepage-text-main'),

                html.A('''PUR-GEN: a tool for polyurethane fragments generation 
                       and its applicability for computational biodegradation studies, 
                       Szleper K., Raczyńska A., Góra A., 2024''', 
                       href='http://www.doi.pl/',className='homepage-publication-link'),
                
              #   html.Img(src='assets/PUR.png',
              #            style={'width': '100%','opacity':'0.3','margin-top': '50px'}),
                html.Img(src='assets/abstract.png',
                         style={'width': '40%','margin-top': '10px', 'margin-bottom':'10px'}),
                         
                html.H3("Contact Information", className = 'contact-info'),
                html.H3("Katarzyna Szleper", className = 'email-info'),
                html.H3("email: k.szleper@tunnelinggroup.pl", className = 'email-info'),
                html.H3("VISIT OUR WEBPAGE!", className = 'tg-info'),
                html.A("Tunneling Group", href='http://www.tunnelinggroup.pl/', 
                       title = 'http://www.tunnelinggroup.pl/', className = 'tg-link'),
                     html.Br()
                ])
])