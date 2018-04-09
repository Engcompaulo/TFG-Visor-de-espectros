from flask import session, redirect, url_for, flash
from flask_dance.contrib.google import google
from SpectraViewer.utils.decorators import google_required
from . import google_bp


@google_bp.route('/logout')
@google_required
def logout():
    keys = list(session)
    for key in keys:
        del(session[key])
    flash('Has cerrado la sesión')
    return redirect(url_for('index'))


@google_bp.route('/after-login')
@google_required
def after_in():
    resp = google.get('/oauth2/v2/userinfo')
    assert resp.ok, resp.text
    email = resp.json()['email']
    session['email'] = email
    return redirect(url_for('index'))
