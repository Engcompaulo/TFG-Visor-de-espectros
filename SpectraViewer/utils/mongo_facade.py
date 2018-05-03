"""
    SpectraViewer.utils.mongo_facade
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module contains uses the facade design pattern to help interact
    with MongoDB.

    :copyright: (c) 2018 by Iván Iglesias
    :license: license_name, see LICENSE for more details
"""
import os
import pandas as pd
from SpectraViewer import mongo


def _filter_dirs(dir_contents):
    dirs = [content for content in dir_contents if content.is_dir()]
    return dirs


def _filter_files(dir_contents, extension):
    files = [content for content in dir_contents
             if content.is_file() and content.name.lower().endswith(extension)]
    return files


def save_dataset(dataset_path, dataset_name, user_id):
    dataset = {'dataset_name': dataset_name, 'user_id': user_id}
    data = dict()
    for directory in _filter_dirs(os.scandir(dataset_path)):
        data[directory.name] = dict()
        for spectrum in _filter_files(os.scandir(directory.path), '.csv'):
            df = pd.read_csv(spectrum.path, delimiter=';', header=None)
            df.columns = ['Raman shift', 'Intensity']
            name = spectrum.name.split('.')[0]
            data[directory.name][name] = df.to_json(orient='split')
    dataset['data'] = data
    mongo.db.datasets.insert_one(dataset)


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
