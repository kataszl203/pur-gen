import dash
from dash import html, dcc
import flask

server = flask.Flask(__name__)
app = dash.Dash(__name__, use_pages=True, server = server, external_stylesheets = ['assets/style.css'])

app.layout = html.Div([
    dcc.Store(id='stored-substrates', data=[]),
    dcc.Store(id='stored-size'),
    dcc.Store(id='stored-capping'),
    dash.page_container
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=False)
