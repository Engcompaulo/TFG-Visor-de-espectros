"""
    SpectraViewer.models
    ~~~~~~~~~~~~~~~~~~~~

    This module contains the models of the application, this way field
    names used in Mongo doesn/t need to be remembered and accessing
    data gets easier.

    :copyright: (c) 2018 by Iván Iglesias
    :license: license_name, see LICENSE for more details
"""


class Dataset(object):

    def __init__(self, name, user, data, notes):
        self.name = name
        self.user = user
        self.data = data
        self.notes = notes


class Spectrum(object):

    def __init__(self, name, user, data, notes):
        self.name = name
        self.user = user
        self.data = data
        self.notes = notes

