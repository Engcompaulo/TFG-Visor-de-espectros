"""
    SpectraViewer.utils.mongo_facade
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module contains uses the facade design pattern to help interact
    with MongoDB.

    :copyright: (c) 2018 by Iván Iglesias
    :license: license_name, see LICENSE for more details
"""
import os
import numpy as np
import pandas as pd
import pickle
from pymongo.errors import DuplicateKeyError

from SpectraViewer import mongo
from SpectraViewer.models import Spectrum, Dataset, ClassifierSet
from SpectraViewer.utils.directories import get_path


def _filter_dirs(dir_contents):
    """
    Return the subdirectories present in a directory.

    Parameters
    ----------
    dir_contents : list
        Directory contents.

    Returns
    -------
    list
        Subdirectories.
    """
    dirs = [content for content in dir_contents if content.is_dir()]
    return dirs


def _filter_files(dir_contents, extension):
    """
    Return the files with the specified extension in a directory.

    Parameters
    ----------
    dir_contents : list
        Directory contents.
    extension : str
        File extension with dot.

    Returns
    -------
    list
        Files with extension.
    """
    files = [content for content in dir_contents
             if content.is_file() and content.name.lower().endswith(extension)]
    return files


def _load_dataset_from_path(path):
    """
    Load the dataset in the given path and create a DataFrame with it
    following the metadata file.

    Parameters
    ----------
    path : str
        Path where the dataset is located.

    Returns
    -------
    dataset : DataFrame
        DataFrame containing the whole dataset and its metadata.

    """
    metadatos = pd.read_excel(get_path(path, "metadatos.xlsx"))
    dataset = pd.DataFrame()
    feature_names = np.arange(50, 2801)

    for label in metadatos['Id']:
        for spectrum in _filter_files(os.scandir(os.path.join(path, label)),
                                      '.csv'):
            data = pd.read_csv(spectrum.path, sep=";", header=None)
            values = data[1].values
            # some spectra start with 0
            if values[0] == 0:
                values[0] = values[1]

            oldx = data[0].values
            values = np.interp(feature_names, oldx, values)

            df = pd.DataFrame(columns=feature_names)
            df.loc[f'{label}/{spectrum.name}'] = values
            df['Etiqueta'] = label
            df['Nombre'] = spectrum.name
            dataset = dataset.append(df)

    dataset = dataset.merge(metadatos, left_on='Etiqueta', right_on='Id')
    dataset = dataset.drop(columns=['Id'])
    return dataset


def _load_spectrum_from_path(path):
    """
    Load the spectrum in the given path and create a DataFrame with it.

    Parameters
    ----------
    path : str
        Path where the spectrum is located.

    Returns
    -------
    df : DataFrame
        DataFrame containing the spectrum.

    """
    feature_names = np.arange(50, 2801)
    spectrum = pd.read_csv(path, sep=';', header=None)
    oldx = spectrum[0].values
    values = spectrum[1].values

    # some spectra start with 0
    if values[0] == 0:
        values[0] = values[1]

    values = np.interp(feature_names, oldx, values)
    df = pd.DataFrame(columns=feature_names)
    df.loc['0'] = values
    return df


def save_dataset(dataset_path, dataset_name, dataset_notes, user_id):
    """
    Save the dataset located in the given path in MongoDB.

    Parameters
    ----------
    dataset_path : str
        Dataset path.
    dataset_name : str
        Dataset name.
    dataset_notes : str
        Notes related the dataset.
    user_id : str
        Id of the user owning the dataset.

    Returns
    -------
    bool
        True if successfully saved, False if the user has a dataset with
        the same name.

    """
    dataset = {'dataset_name': dataset_name, 'dataset_notes': dataset_notes,
               'user_id': user_id}
    data = _load_dataset_from_path(dataset_path)
    dataset['data'] = data.to_json(orient='split')  # Split to mantains order
    try:
        mongo.db.datasets.insert_one(dataset)
        return True
    except DuplicateKeyError:
        return False


def save_spectrum(spectrum_path, spectrum_name, spectrum_notes, user_id):
    """
    Save the dataset located in the given path in MongoDB.

    Parameters
    ----------
    spectrum_path : str
        Spectrum path.
    spectrum_name : str
        Spectrum name.
    spectrum_notes : str
        Notes related the Spectrum.
    user_id : str
        Id of the user owning the Spectrum.

    Returns
    -------
    bool
        True if successfully saved, False if the user has a spectrum
        with the same name.

    """
    spectrum = {'spectrum_name': spectrum_name,
                'spectrum_notes': spectrum_notes,
                'user_id': user_id}
    data = _load_spectrum_from_path(spectrum_path)
    spectrum['data'] = data.to_json(orient='split')  # Split to mantain order
    try:
        mongo.db.spectra.insert_one(spectrum)
        return True
    except DuplicateKeyError:
        return False


def get_datasets(user_id):
    """
    Return all datasets a given user owns.

    Parameters
    ----------
    user_id : str
        User id.

    Returns
    -------
    list
        User datasets.

    """
    datasets_temp = mongo.db.datasets.find({'user_id': user_id})
    datasets = []
    for d in datasets_temp:
        datasets.append(Dataset(d['dataset_name'], d['user_id'], d['data'],
                                d['dataset_notes']))
    return datasets


def get_spectra(user_id):
    """
    Return all spectra a given user owns.

    Parameters
    ----------
    user_id : str
        User id.

    Returns
    -------
    list
        User spectra.

    """
    spectra_temp = mongo.db.spectra.find({'user_id': user_id})
    spectra = []
    for s in spectra_temp:
        spectra.append(Spectrum(s['spectrum_name'], s['user_id'], s['data'],
                                s['spectrum_notes']))
    return spectra


def get_user_dataset(dataset_name, user_id):
    """
    Return the dataset with the given name belonging to the given user.

    Parameters
    ----------
    dataset_name : str
        Dataset name.
    user_id : str
        User id.

    Returns
    -------
    DataFrame
        DataFrame containing the dataset.

    """
    dataset = mongo.db.datasets.find_one({'dataset_name': dataset_name,
                                          'user_id': user_id})
    data = pd.read_json(dataset['data'], orient='split')
    return data


def get_user_spectrum(spectrum_name, user_id):
    """
    Return the dataset with the given name belonging to the given user.

    Parameters
    ----------
    spectrum_name : str
        Spectrum name.
    user_id : str
        User id.

    Returns
    -------
    DataFrame
        DataFrame containing the spectrum.

    """
    spectrum = mongo.db.spectra.find_one({'spectrum_name': spectrum_name,
                                          'user_id': user_id})
    data = pd.read_json(spectrum['data'], orient='split')
    return data


def remove_dataset(dataset_name, user_id):
    """
    Remove from Mongo the dataset with the given name belonging to the
    given user. However, this does not remove it from disk storage.

    Parameters
    ----------
    dataset_name : str
        Dataset name.
    user_id : str
        User id.

    """
    mongo.db.datasets.delete_one({'dataset_name': dataset_name,
                                  'user_id': user_id})


def remove_spectrum(spectrum_name, user_id):
    """
    Remove from Mongo the spectrum with the given name belonging to the
    given user. However, this does not remove it from disk storage.

    Parameters
    ----------
    spectrum_name : str
        Spectrum name.
    user_id : str
        User id.

    """
    mongo.db.spectra.delete_one({'spectrum_name': spectrum_name,
                                 'user_id': user_id})


def save_classifiers(classifiers):
    """Save the given classifiers object to Mongo.

    Parameters
    ----------
    classifiers : ClassifierSet
        Class containing all data of the classifiers.

    Returns
    -------
    bool
        True if saved, False if name and user is already saved.

    """
    classifiers_document = {'classifiers_name': classifiers.name,
                            'classifiers_notes': classifiers.notes,
                            'user_id': classifiers.user,
                            'mine': pickle.dumps(classifiers.mine),
                            'prof': pickle.dumps(classifiers.prof),
                            'pnum': pickle.dumps(classifiers.pnum)}
    try:
        mongo.db.models.insert_one(classifiers_document)
        return True
    except DuplicateKeyError:
        return False


def get_classifiers(user_id):
    """
    Return all spectra a given user owns.

    Parameters
    ----------
    user_id : str
        User id.

    Returns
    -------
    list

    """
    classifiers = list()
    for document in mongo.db.models.find({'user_id': user_id}):
        classifiers.append(ClassifierSet(document['classifiers_name'],
                                         document['user_id'],
                                         document['classifiers_notes'],
                                         pickle.loads(document['mine']),
                                         pickle.loads(document['prof']),
                                         pickle.loads(document['pnum'])))
    return classifiers


def get_classifier(classifier_name, user_id):
    """
    Return all spectra a given user owns.

    Parameters
    ----------
    classifier_name : str
        Classifiers object name.
    user_id : str
        User id.

    Returns
    -------
    ClassifierSet

    """
    document = mongo.db.models.find_one({'classifiers_name': classifier_name,
                                         'user_id': user_id})
    return ClassifierSet(document['classifiers_name'],
                         document['user_id'],
                         document['classifiers_notes'],
                         pickle.loads(document['mine']),
                         pickle.loads(document['prof']),
                         pickle.loads(document['pnum']))


def remove_classifiers(classifiers_name, user_id):
    """
    Remove from Mongo the classifiers object with the given name
     belonging to the given user.

    Parameters
    ----------
    classifiers_name : str
        Spectrum name.
    user_id : str
        User id.

    """
    mongo.db.models.delete_one({'classifiers_name': classifiers_name,
                                'user_id': user_id})
