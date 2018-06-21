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


class ClassifierSet(object):
    """This class stores all three possible classifiers along with other
    attributes.

    Attributes
    ----------
    name : str
        Name of the classifier set.
    user : str
        User who owns the classifier set.
    notes : str
        Notes related to the classifier.
    mine : scikit-learn model
        Trained model which predicts "Mina" attribute.
    prof : scikit-learn model
        Trained model which predicts "Profundidad" attribute.
    pnum : scikit-learn model
        Trained model which predicts "Profundidad_num" attribute.
    """

    def __init__(self, name, user, notes, mine_classifier, prof_classifier,
                 pnum_classifier):
        self.name = name
        self.user = user
        self.notes = notes
        self.mine = mine_classifier
        self.prof = prof_classifier
        self.pnum = pnum_classifier
