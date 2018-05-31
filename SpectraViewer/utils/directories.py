"""
    SpectraViewer.utils.directories
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module contains functions that help in the task of searching
    through the directories.

    :copyright: (c) 2018 by Iván Iglesias
    :license: license_name, see LICENSE for more details
"""
import os
from flask import current_app, session


def get_temp_directory():
    """
    Get the path for the temporary directory.

    Returns
    -------
    str
        Temporary directory.

    """
    temp_directory = os.path.join(current_app.instance_path,
                                  current_app.config['UPLOAD_FOLDER'], 'temp')
    _create_if_not_exists(temp_directory)
    return temp_directory


def _create_if_not_exists(directory):
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


def get_path(directory, name):
    """
    Get the full path of a file or folder contained inside a directory.

    Parameters
    ----------
    directory : str
        Directory.
    name : str
        Name of the folder of file.

    Returns
    -------
    str
        Path inside the directory.

    """
    return os.path.join(directory, name)


def get_user_directory():
    """
    Get the directory which belongs the current user,

    Returns
    -------
    str
        Path of the directory.

    """
    user_directory = os.path.join(current_app.instance_path,
                                  current_app.config['UPLOAD_FOLDER'],
                                  str(session['user_id']))
    _create_if_not_exists(user_directory)
    return user_directory
