"""
    SpectraViewer.auth.routes
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    This module contains the routes for the auth blueprint.

    :copyright: (c) 2018 by Iván Iglesias
    :license: license_name, see LICENSE for more details
"""
from flask import session, redirect, url_for, flash
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
        del(session[key])
    flash('Has cerrado la sesión')
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
    assert resp.ok, resp.text
    email = resp.json()['email']
    session['email'] = email
    return redirect(url_for('main.index'))
