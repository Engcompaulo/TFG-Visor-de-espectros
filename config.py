"""
    config
    ~~~~~~

    This file contains classes to be used as the configuration for the
    app.

    :copyright: (c) 2018 by Iván Iglesias
    :license: license_name, see LICENSE for more details
"""
import os


class Config(object):
    GOOGLE_OAUTH_CLIENT_ID = os.environ.get('GOOGLE_OAUTH_CLIENT_ID')
    GOOGLE_OAUTH_CLIENT_SECRET = os.environ.get('GOOGLE_OAUTH_CLIENT_SECRET')
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER')
    SECRET_KEY = os.environ.get('SECRET_KEY')


class DevelopmentConfig(Config):
    DATA_MONGODB_HOST = 'localhost'
    MONGO_URI = f'mongodb://{DATA_MONGODB_HOST}:27017/'


class ProductionConfig(Config):
    DATA_MONGODB_HOST = os.environ.get('DATA_MONGODB_HOST')
    MONGO_URI = f'mongodb://{DATA_MONGODB_HOST}:27017/'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
