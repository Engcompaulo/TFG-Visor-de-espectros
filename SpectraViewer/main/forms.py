"""
    SpectraViewer.main.forms
    ~~~~~~~~~~~~~~~~~~~~~~~~

    This file contains the forms used by the main module.

    :copyright: (c) 2018 by Iván Iglesias
    :license: license_name, see LICENSE for more details
"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField


class CsvForm(FlaskForm):
    """Form for handling file upload.

    Attributes
    ----------
    file : FileField
        Allows the user to upload a file to the server. Only .csv
        files are allowed, can't be empty.
    submit : SubmitField
        Input field of type submit to trigger the upload action.

    """
    _validators = [
        FileRequired('Es obligatorio seleccionar un fichero'),
        FileAllowed(['csv'], 'Solo ficheros .csv')
    ]
    file = FileField(label='Fichero csv', validators=_validators)
    submit = SubmitField('Subir')
