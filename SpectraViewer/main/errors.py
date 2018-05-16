"""
    SpectraViewer.main.errors
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    This file contains the error handlers of the application.

    :copyright: (c) 2018 by Iván Iglesias
    :license: license_name, see LICENSE for more details
"""
from flask import render_template
from . import main


@main.app_errorhandler(404)
def page_not_found(e):
    """
    Render the view for the not found error.

    Parameters
    ----------
    e

    Returns
    -------
    Render error 404 view.

    """
    return render_template('errors/404.html'), 404


@main.app_errorhandler(500)
def internal_error(e):
    """
    Render the view for the internal server error.

    Parameters
    ----------
    e

    Returns
    -------
    Render error 500 view.

    """
    return render_template('errors/500.html'), 500
