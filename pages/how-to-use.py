import dash
from dash import html, dcc

dash.register_page(__name__, path='/how-to-use')

# Define layout for the "How to Use" page
layout = html.Center(style = {'display': 'block','alignItems': 'center',},
    children = [
        html.Center(className='how-to-use-page-header',children = [
            html.A(html.Img(src='assets/pur-gen.png', className = 'homepage-logo'),href='/',id='top'),
                    html.Div(className='header-buttons',children=[
                        dcc.Link(html.Button('HOME PAGE'), href='/'),
                        dcc.Link(html.Button('RUN PUR-GEN'), href='/run')]),
                    ]),

    html.H2("HOW IT WORKS?", className = 'highlighted-center-text'),

    html.H3('''PUR-GEN allows one to generate short fragments of polyurethanes (PUR) 
            for further use. Follow the steps to obtain the structures:''', 
            className='center-text'),

    html.Div(children = [html.Div(className='circle-pink')], className='how-to-use-circle'),
    
    html.H2("1. SELECT OR UPLOAD SUBSTRATES",className='highlighted-center-smaller-text'),
    
    html.Div([html.Img(src='assets/substrates.png',
                       style={'max-width': '60%'})],
                       className='how-to-use-image'),

    html.H3('''PUR fragments can be generated from diverse groups of both main 
            substrates used for PUR synthesis: isocyanates and hydroxyl compounds. 
            Most commonly used substrates are provided on the website.''', 
            className='center-text'),

    html.Img(src='assets/select-substrates.png', className='how-to-use-screenshot'),

    html.H3('''To generate other desired motifs, one can also upload other 
            substrate structures in SMILES format. 
            Input file should be prepared as the following example:''', 
            className='center-text'),

    html.Img(src='assets/test-input.png', className='how-to-use-screenshot-no-border'),

    html.Div(children = [html.Div(className='circle-grey')],className='how-to-use-circle'),

    html.H2("2. SELECT PARAMETERS: SIZE AND CAPPING GROUPS",className='highlighted-center-smaller-text'),
    
    html.Div([html.Img(src='assets/sizes.png',
                        style={'max-width': '60%'})],
                        className='how-to-use-image'),
    html.H3(''' Users can define the length of generated PUR fragments based 
            on the number of substrate being used (2,3 or 4 units). 
            2 units correspond to a PUR monomer and 4 units correspond to a PUR dimer.''', 
            className='center-text'),

    html.H3('''To reflect the experimental conditions and prevent from undesirable 
            behaviour of generated structures, free isocyanate groups can be 
            neutralized by capping them with -CH3, -NH2 or -NH(C=O)OH.''', 
            className='center-text'), 

    html.Img(src='assets/select-size.png', className='how-to-use-screenshot'),    
    html.H3('''These are the only input settings needed to run the program.''', 
            className='center-text'),                
    
    html.Div(children = [html.Div(className='circle-purple')],className='how-to-use-circle'),
    
    html.H2("3. RESULTS",className='highlighted-center-smaller-text'),

    html.Div([html.Img(src='assets/downloads.png',
                        style={'max-width': '30%'})],
                        className='how-to-use-image'),

    html.H3('''PUR-GEN generates a summary and short analysis of obtained compounds. 
            In a tab "PUR structures" are presented structures of geneated PUR fragments.
            Tab "Calculated properties" contains information about molecular weight, 
            number of heavy atoms,
            number of rotatable bonds, presence of ester bond, presence of ether bond,
            number of aromatic atoms, aromatic proportion (number of aromatic atoms 
            divided by number of heavy atoms), Crippen-Wildman partition coefficient (clogP),
            topological polar surface area (TPSA), Crippen-Wildman molar refractivity (MR).
            Tab "Properties histograms" shows the calculated data on plots.  
            ''', 
            className='center-text'),
            
    html.H3('''Calculated properties can be downloaded as a table in .csv file format. 
            User can download generated structures in .mol and .mol2 file formats.
            It is also possible to generate up to 20 conformers, however, 
            if the number of generated compounds is high, this action may take a while.''', 
            className='center-text'),

    html.Img(src='assets/results.png', className='how-to-use-screenshot-margin'),

    html.Div(dcc.Link(html.Button("back to top of the page"), href='#top')),

    html.Br(),
    html.H3("Contact Information", className = 'contact-info'),
    html.H3("Katarzyna Szleper", className = 'email-info'),
    html.H3("email: k.szleper@tunnelinggroup.pl", className = 'email-info'),
    html.H3("VISIT OUR WEBPAGE!", className = 'tg-info'),
    html.A("Tunneling Group", href='http://www.tunnelinggroup.pl/', 
                       title = 'http://www.tunnelinggroup.pl/', className = 'tg-link'),
    html.Br()
    ])