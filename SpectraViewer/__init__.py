"""
    SpectraViewer
    ~~~~~~~~~~~~~

    Web application to help people deal with visualization and
    processing of spectra.

    :copyright: (c) 2018 by Iván Iglesias
    :license: license_name, see LICENSE for more details
"""
import os

from flask import Flask
from flask_bootstrap import Bootstrap
import pymongo
from flask_pymongo import PyMongo

import config
from SpectraViewer.visualization.app import create_dash_app

bootstrap = Bootstrap()
mongo = PyMongo()


def create_app():
    app = Flask(__name__)
    config_name = os.environ.get('ENVIRONMENT') or 'default'
    app.config.from_object(config.config[config_name])

    create_dash_app(app)

    from SpectraViewer.auth import google_bp
    app.register_blueprint(google_bp, url_prefix="/auth")

    from SpectraViewer.main import main as main_bp
    app.register_blueprint(main_bp)

    _init_extensions(app)
    return app


def _init_extensions(app):
    bootstrap.init_app(app)
    mongo.init_app(app)

    with app.app_context():
        mongo.db.datasets.create_index([('dataset_name', pymongo.ASCENDING)],
                                       unique=True)
