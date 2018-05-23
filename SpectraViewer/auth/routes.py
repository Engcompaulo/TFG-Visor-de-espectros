"""
    SpectraViewer.auth.routes
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    This module contains the routes for the auth blueprint.

    :copyright: (c) 2018 by Iván Iglesias
    :license: license_name, see LICENSE for more details
"""
from flask import session, redirect, url_for, flash, abort
from flask_dance.contrib.google import google
from SpectraViewer.utils.decorators import google_required
from . import google_bp


@google_bp.route('/logout')
@google_required
def logout():
    """
    Log out of the app by deleting the stored cookies.

    Returns
    -------
        Redirect to index page.

    """
    keys = list(session)
    for key in keys:
        del (session[key])
    flash('Se ha cerrado correctamente la sesión', 'success')
    return redirect(url_for('main.index'))


@google_bp.route('/after-login')
@google_required
def after_in():
    """
    Get user email and store it to avoid repeating requests to Google.

    Returns
    -------
        Redirect to index page.

    """
    resp = google.get('/oauth2/v2/userinfo')
    if not resp.ok and not resp.text:
        flash('Ha habido un problema de conexión con Google', 'danger')
        abort(500)
    email = resp.json()['email']
    user_id = resp.json()['id']
    name = resp.json()['name']
    session['email'] = email
    session['user_id'] = user_id
    session['name'] = name
    return redirect(url_for('main.index'))
