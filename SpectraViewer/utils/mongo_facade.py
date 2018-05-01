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


def save_dataset_to_mongo(dataset_path, dataset_name, user_id):
    dataset = {'dataset_name': dataset_name, 'user_id': user_id}
    for directory in filter(lambda content: content.is_dir(),
                            os.scandir(dataset_path)):
        dataset[directory.name] = dict()
        for spectrum in filter(lambda content: content.is_file and content.name.lower().endswith('.csv'), os.scandir(directory.path)):
            df = pd.read_csv(spectrum.path, delimiter=';', header=None)
            df.columns = ['Raman shift', 'Intensity']
            name = spectrum.name.split('.')[0]
            dataset[directory.name][name] = df.to_json()

    mongo.db.datasets.insert_one(dataset)
