"""
    SpectraViewer.main
    ~~~~~~~~~~~~~~~~~~

    Main module of the applicaton.

    :copyright: (c) 2018 by Iván Iglesias
    :license: license_name, see LICENSE for more details
"""
from flask import Blueprint

main = Blueprint('main', __name__)

from . import routes, errors
