"""
    SpectraViewer.main.forms
    ~~~~~~~~~~~~~~~~~~~~~~~~

    This file contains the forms used by the main module.

    :copyright: (c) 2018 by Iván Iglesias
    :license: license_name, see LICENSE for more details
"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField, StringField, TextAreaField
from wtforms.validators import DataRequired


class SpectrumForm(FlaskForm):
    """Form for handling spectrum upload.

    Attributes
    ----------
    name : StringField
        Field with the spectrum name. Required.
    notes : TextAreaField
        Field with the dataset notes. Optional.
    file : FileField
        Allows the user to upload a file to the server. Only .csv
        files are allowed, can't be empty.
    submit : SubmitField
        Input field of type submit to trigger the upload action.

    """
    _name_validators = [DataRequired('Es obligatorio poner nombre al espectro')]
    _file_validators = [
        FileRequired('Es obligatorio seleccionar un fichero'),
        FileAllowed(['csv'], 'Solo se admiten ficheros csv')
    ]
    name = StringField('Nombre del espectro', validators=_name_validators)
    notes = TextAreaField(label='Comentarios sobre el espectro')
    file = FileField(label='Seleccione un espectro',
                     validators=_file_validators,
                     render_kw={'onchange': 'setFileName()'})
    submit = SubmitField('Subir', render_kw={'data-toggle': 'modal',
                                             'data-target': '#waiting-modal',
                                             'data-backdrop': 'static',
                                             'data-keyboard': 'false'})


class DatasetForm(FlaskForm):
    """Form for handling dataset upload.

    Attributes
    ----------
    name : StringField
        Field with the dataset name. Required.
    notes : TextAreaField
        Field with the dataset notes. Optional.
    file : FileField
        Field with the dataset file. Required, can only be a zip file.
    submit : SubmitField
        Input field of type submit to trigger the upload action.

    """
    _name_validators = [
        DataRequired('Es obligatorio poner nombre al dataset')]
    _file_validators = [
        FileRequired('Es obligatorio seleccionar un fichero'),
        FileAllowed(['zip'], 'Solo se admiten ficheros zip')
    ]
    name = StringField(label='Nombre del dataset',
                       validators=_name_validators)
    notes = TextAreaField(label='Comentarios sobre el dataset')
    file = FileField(label='Seleccione un dataset',
                     validators=_file_validators,
                     render_kw={'onchange': 'setFileName()'})
    submit = SubmitField('Subir', render_kw={'data-toggle': 'modal',
                                             'data-target': '#waiting-modal',
                                             'data-backdrop': 'static',
                                             'data-keyboard': 'false'})


class ClassifierForm(FlaskForm):
    """Form for entering the classiffiers object name and notes.

    Attributes
    ----------
    name : StringField
        Field with the classifier name. Required.
    notes : TextAreaField
        Field with the dataset notes. Optional.

    """
    _name_validators = [
        DataRequired('Es obligatorio poner nombre al clasificador')]
    name = StringField(label='Nombre del clasificador',
                       validators=_name_validators)
    notes = TextAreaField(label='Comentarios sobre el clasificador')
