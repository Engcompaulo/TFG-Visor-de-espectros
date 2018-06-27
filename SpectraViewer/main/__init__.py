"""
    SpectraViewer.main
    ~~~~~~~~~~~~~~~~~~

    Main module of the applicaton.

    :copyright: (c) 2018 by Iván Iglesias
    :license: GPL-3.0, see LICENSE for more details
"""
from flask import Blueprint

main = Blueprint('main', __name__)

from . import routes, errors
