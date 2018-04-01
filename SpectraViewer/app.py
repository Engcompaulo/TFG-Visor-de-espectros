"""
    SpectraViewer.app
    ~~~~~~~~~~~~~~~~~

    This is just a prototype for the full application. Right now all
    code is contained in this file, this is intended to change in the
    future.

    :copyright: (c) 2018 by Iván Iglesias
    :license: license_name, see LICENSE for more details
"""
from flask import Flask
from flask_bootstrap import Bootstrap

import dash
import dash_html_components as html

server = Flask(__name__)
bootstrap = Bootstrap(server)

app = dash.Dash(__name__, server=server, url_base_pathname='/plot')
app.title = 'Aplicación Dash'
app.layout = html.Div()  # Needs a layout, so empty layout is good to go
app.scripts.append_script({'external_url': [
    'http://cdnjs.cloudflare.com/ajax/libs/jquery/1.12.4/jquery.min.js',
    'http://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/js/bootstrap.min.js']})

app.css.append_css({
    'external_url': 'http://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/css/bootstrap.min.css'})

server.config['SECRET_KEY'] = 'secret key'
server.config['UPLOAD_FOLDER'] = 'csvs'

from SpectraViewer import routes

if __name__ == '__main__':
    app.run_server(debug=True)
