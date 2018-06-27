"""
    start
    ~~~~~

    Launch the web applicaction.

    :copyright: (c) 2018 by Iván Iglesias
    :license: GPL-3.0, see LICENSE for more details
"""
from SpectraViewer import create_app

app = create_app()

if __name__ == '__main__':
    app.run(ssl_context='adhoc')
