"""
    SpectraViewer.utils.decorators
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module contains function decorators useful for the application.

    :copyright: (c) 2018 by Iván Iglesias
    :license: license_name, see LICENSE for more details
"""
from functools import wraps
from flask import flash, redirect, url_for
from flask_dance.contrib.google import google


def google_required(controller):
    @wraps(controller)
    def decorated_function(*args, **kwargs):
        if not google.authorized:
            flash('Necesita iniciar sesión para acceder a la página')
            return redirect(url_for('main.index'))
        else:
            return controller(*args, **kwargs)
    return decorated_function
