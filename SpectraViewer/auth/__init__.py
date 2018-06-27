"""
    SpectraViewer.auth
    ~~~~~~~~~~~~~~~~~~

    This module provides the application of all it needs to use OAuth2
    with Google.

    :copyright: (c) 2018 by Iván Iglesias
    :license: GPL-3.0, see LICENSE for more details
"""
from flask_dance.contrib.google import make_google_blueprint

google_bp = make_google_blueprint(scope=['email', 'profile'],
                                  reprompt_consent=True,
                                  redirect_to='google.after_in')

from . import routes
