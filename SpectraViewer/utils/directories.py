"""
    SpectraViewer.utils.directories
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module contains functions that help in the task of searching
    through the directories.

    :copyright: (c) 2018 by Iván Iglesias
    :license: license_name, see LICENSE for more details
"""
import os
from flask import current_app


def get_temp_directory():
    """
    Get the path for the temporary directory.

    Returns
    -------
    str
        Temporary directory.

    """
    return os.path.join(current_app.instance_path,
                        current_app.config['UPLOAD_FOLDER'], 'temp')


def create_if_not_exists(directory):
    """
    Create the given directory and subdirectories in case none of them
    exist.

    Parameters
    ----------
    directory : str
        Directory to be created.

    """
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_file_path(directory, filename):
    """
    Get the full path of a file contained inside a directory.

    Parameters
    ----------
    directory : str
        Directory.
    filename : str
        Filename.

    Returns
    -------
    str
        Path of the file in the directory.

    """
    return os.path.join(directory, filename)


def get_user_directory(user_id):
    """
    Get the directory which belongs the user with the given id.

    Parameters
    ----------
    user_id : int
        Id of the user.

    Returns
    -------
    str
        Path of the directory.

    """
    return os.path.join(current_app.instance_path,
                        current_app.config['UPLOAD_FOLDER'], str(user_id))


def get_user_datasets(user_directory):
    """
    Get a list containing the name of the datasets in the given directory.

    Parameters
    ----------
    user_directory : str
        Directory of a user.

    Returns
    -------
    list
        List of strings.

    """
    user_contents = list(map(lambda content:
                             os.path.join(user_directory, content),
                             os.listdir(user_directory)))
    user_datasets = list(filter(lambda content:
                                os.path.isdir(content),
                                user_contents))
    return list(map(lambda dataset: os.path.split(dataset)[-1], user_datasets))
