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

from config import Config
from SpectraViewer.auth import google_bp

server = Flask(__name__)
server.config.from_object(Config)
bootstrap = Bootstrap(server)

server.register_blueprint(google_bp, url_prefix="/auth")

app = dash.Dash(__name__, server=server, url_base_pathname='/plot')

app.layout = html.Div()

from SpectraViewer import routes


if __name__ == '__main__':
    app.run_server(debug=True)
