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
from flask_dance.contrib.google import make_google_blueprint

import dash
import dash_html_components as html

from config import Config

server = Flask(__name__)
server.config.from_object(Config)
bootstrap = Bootstrap(server)
blueprint = google_bp = make_google_blueprint(scope=["profile", "email"])
server.register_blueprint(google_bp, url_prefix="/auth")

app = dash.Dash(__name__, server=server, url_base_pathname='/plot')
app.layout = html.Div()  # Needs a layout, so empty layout is good to go
app.scripts.append_script({'external_url': [
    'http://cdnjs.cloudflare.com/ajax/libs/jquery/1.12.4/jquery.min.js',
    'http://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/js/bootstrap.min.js']})

app.css.append_css({
    'external_url': 'http://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/css/bootstrap.min.css'})

from SpectraViewer import routes

if __name__ == '__main__':
    app.run_server(debug=True)
