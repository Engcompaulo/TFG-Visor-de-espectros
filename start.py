"""
    start
    ~~~~~

    Launch the web applicaction.

    :copyright: (c) 2018 by Iván Iglesias
    :license: license_name, see LICENSE for more details
"""
from SpectraViewer.app import server

if __name__ == '__main__':
    server.run(debug=True)
