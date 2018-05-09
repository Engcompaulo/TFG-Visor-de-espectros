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
from pymongo.errors import DuplicateKeyError

from SpectraViewer import mongo
from SpectraViewer.utils.directories import get_path


def _filter_dirs(dir_contents):
    dirs = [content for content in dir_contents if content.is_dir()]
    return dirs


def _filter_files(dir_contents, extension):
    files = [content for content in dir_contents
             if content.is_file() and content.name.lower().endswith(extension)]
    return files


def _load_dataset_from_path(path):
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
            df['Label'] = label
            df['Name'] = spectrum.name
            dataset = dataset.append(df)

    dataset = dataset.merge(metadatos, left_on='Label', right_on='Id')
    dataset = dataset.drop(columns=['Id'])
    return dataset


def save_dataset(dataset_path, dataset_name, dataset_notes, user_id):
    dataset = {'dataset_name': dataset_name, 'dataset_notes': dataset_notes,
               'user_id': user_id}
    data = _load_dataset_from_path(dataset_path)
    dataset['data'] = data.to_json(orient='split')
    try:
        mongo.db.datasets.insert_one(dataset)
        return True
    except DuplicateKeyError:
        return False


def get_datasets(user_id):
    datasets = mongo.db.datasets.find({'user_id': user_id})
    return datasets


def get_user_dataset(dataset_name, user_id):
    dataset = mongo.db.datasets.find_one({'dataset_name': dataset_name,
                                          'user_id': user_id})
    data = dataset['data']
    return data


def remove_dataset(dataset_name, user_id):
    mongo.db.datasets.delete_one({'dataset_name': dataset_name,
                                  'user_id': user_id})
