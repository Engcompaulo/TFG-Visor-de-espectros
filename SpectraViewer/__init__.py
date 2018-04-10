"""
    SpectraViewer
    ~~~~~~~~~~~~~

    Web application to help people deal with representation and
    processing of spectra.

    :copyright: (c) 2018 by Iván Iglesias
    :license: license_name, see LICENSE for more details
"""
from flask import Flask
from flask_bootstrap import Bootstrap

from config import Config
from SpectraViewer.representation import create_dash_app

bootstrap = Bootstrap()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    create_dash_app(app)

    from SpectraViewer.auth import google_bp
    app.register_blueprint(google_bp, url_prefix="/auth")

    from SpectraViewer.main import main as main_bp
    app.register_blueprint(main_bp)

    bootstrap.init_app(app)
    return app
