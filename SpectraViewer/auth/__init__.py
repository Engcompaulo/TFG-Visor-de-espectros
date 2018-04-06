"""
    SpectraViewer.auth
    ~~~~~~~~~~~~~~~~~~

    This module

    :copyright: (c) 2018 by Iván Iglesias
    :license: license_name, see LICENSE for more details
"""
from flask_dance.contrib.google import make_google_blueprint

google_bp = make_google_blueprint(scope=["email"], reprompt_consent=True,
                                  redirect_to='google.after_in')

from . import routes
