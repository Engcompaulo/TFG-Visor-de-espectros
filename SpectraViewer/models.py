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
    """Class that represents a dataset.

    Attributes
    ----------
    name : str
        Name of the dataset.
    user : str
        Id of the user who owns the dataset.
    data : DataFrame
        Pandas DataFrame which contains the dataset.
    notes : str
        Notes related to the dataset.

    """
    def __init__(self, name, user, data, notes):
        self.name = name
        self.user = user
        self.data = data
        self.notes = notes


class Spectrum(object):
    """Class that represents a spectrum.

    Attributes
    ----------
    name : str
        Name of the spectrum.
    user : str
        Id of the user who owns the spectrum.
    data : DataFrame
        Pandas DataFrame which contains the spectrum.
    notes : str
        Notes related to the spectrum.

    """
    def __init__(self, name, user, data, notes):
        self.name = name
        self.user = user
        self.data = data
        self.notes = notes

