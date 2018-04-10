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
    UPLOAD_FOLDER_CSV = os.environ.get('UPLOAD_FOLDER_CSV')
    UPLOAD_FOLDER_ZIP = os.environ.get('UPLOAD_FOLDER_ZIP')
    SECRET_KEY = os.environ.get('SECRET_KEY')
