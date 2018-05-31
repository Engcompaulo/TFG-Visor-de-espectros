"""
    SpectraViewer.main.routes
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    This file contains the routes of the main module.

    :copyright: (c) 2018 by Iván Iglesias
    :license: license_name, see LICENSE for more details
"""
from flask import render_template, redirect, url_for, request, session, flash, \
    send_from_directory, current_app
from werkzeug.utils import secure_filename
from zipfile import ZipFile

from SpectraViewer.main import main
from SpectraViewer.main.forms import SpectrumForm, DatasetForm
from SpectraViewer.utils.decorators import google_required
from SpectraViewer.utils.mongo_facade import save_dataset, remove_dataset, \
    get_datasets, save_spectrum, get_spectra, remove_spectrum
from SpectraViewer.utils.directories import get_temp_directory, get_path, \
    get_user_directory


@main.before_app_request
def before_request():
    """Force the use of https.

    Before every request change the http url to https. If already in
    https this does nothing, just check.

    Returns
    -------
        Redirect to the secure url.

    """
    if request.url.startswith('http://'):
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)


@main.route('/')
@main.route('/index')
def index():
    """Render the index view.

    Welcome or index page of this web app.

    Returns
    -------
    Rendered index view.

    """
    return render_template('index.html')


@main.route('/manage')
@google_required
def manage():
    """Render for the manage view.

    This view contains two lists, one with the uploadet datasets and
    the other with the uploaded spectra. In addition, provides the
    links for the upload dataset veiw and upload spectrum view.

    Returns
    -------
    Rendered manage view.

    """
    user_id = session['user_id']
    user_datasets = [{'name': dataset['dataset_name'],
                      'notes': dataset['dataset_notes']} for dataset in
                     get_datasets(user_id)]
    user_spectra = [{'name': spectrum['spectrum_name'],
                     'notes': spectrum['spectrum_notes']} for spectrum in
                    get_spectra(user_id)]
    return render_template('manage.html', datasets=user_datasets,
                           spectra=user_spectra)


@main.route('/download-template', methods=['GET', 'POST'])
@google_required
def download_template():
    """
    Download to the user the metadata template.

    Returns
    -------
    file
        Return the metadata template to the user.

    """
    return send_from_directory(current_app.root_path, 'metadatos.xlsx',
                               as_attachment=True)


@main.route('/datasets/upload', methods=['GET', 'POST'])
@google_required
def upload_dataset():
    """Render the upload dataset view.

    This page contains a form for uploading datasets, contains
    instructions on how the zip should be composed. If POST, uploads the
    file and extracts it to the user directory with the name provided in
    the form, then it's saved in Mongo.

    Returns
    -------
    Rendered upload dataset view if GET, redirect to manage view if POST.

    """
    form = DatasetForm()
    if form.validate_on_submit():
        f = form.file.data
        filename = secure_filename(f.filename)
        temp_directory = get_temp_directory()
        user_directory = get_user_directory()
        file_path = get_path(temp_directory, filename)
        f.save(file_path)
        dataset_name = form.name.data
        dataset_notes = form.notes.data
        dataset_path = get_path(user_directory, dataset_name)
        with ZipFile(file_path, 'r') as zip_file:
            zip_file.extractall(dataset_path)
        if save_dataset(dataset_path, dataset_name, dataset_notes,
                        session['user_id']):
            flash('Se ha subido el dataset correctamente', 'success')
            return redirect(url_for('main.manage'))
        else:
            flash('Ya se ha subido un dataset con ese nombre'
                  ', use un nombre diferente', 'danger')
            return redirect(url_for('main.upload_dataset'))
    return render_template('upload_dataset.html', form=form)


@main.route('/spectrum/upload', methods=['GET', 'POST'])
@google_required
def upload_spectrum():
    """Render the upload spectrum view.

    This page contains a form for uploading spectum. If POST, uploads
    the file and saves it to the user directory with the name
    provided in the form.

    Returns
    -------
    Rendered upload spectrum view if GET, redirect to manage view if
    POST.

    """
    form = SpectrumForm()
    if form.validate_on_submit():
        f = form.file.data
        filename = secure_filename(f.filename)
        user_directory = get_user_directory()
        file_path = get_path(user_directory, filename)
        f.save(file_path)
        spectrum_notes = form.notes.data
        spectrum_name = form.name.data
        if save_spectrum(file_path, spectrum_name, spectrum_notes,
                         session['user_id']):
            flash('Se ha subido el espectro correctamente', 'success')
            return redirect(url_for('main.manage'))
        else:
            flash('Ya se ha subido un espectro con ese nombre'
                  ', use un nombre diferente', 'danger')
            return redirect(url_for('main.upload_spectrum'))
    return render_template('upload_spectrum.html', form=form)


@main.route('/datasets/edit/<dataset>')
@google_required
def edit_dataset(dataset):
    return 'Not yet implemented'


@main.route('/datasets/delete/<dataset>')
@google_required
def delete_dataset(dataset):
    """
    Remove the dataset with the given name from the database.

    Parameters
    ----------
    dataset : str
        Dataset name.

    Returns
    -------
    Redirect to the manage view.

    """
    remove_dataset(dataset, session['user_id'])
    flash('Se ha borrado correctamente el dataset', 'success')
    return redirect(url_for('main.manage'))


@main.route('/spectrum/delete/<spectrum>')
@google_required
def delete_spectrum(spectrum):
    """
    Remove the spectrum with the given name from the database.

    Parameters
    ----------
    spectrum : str
        Spectrum name.

    Returns
    -------
    Redirect to the manage view.

    """
    remove_spectrum(spectrum, session['user_id'])
    flash('Se ha borrado correctamente el espectro', 'success')
    return redirect(url_for('main.manage'))


@main.route('/datasets/plot/<dataset>')
@google_required
def plot_dataset(dataset):
    """
    Redirect the user to the visualization page with the given dataset.

    Parameters
    ----------
    dataset : str
        Dataset name.

    Returns
    -------
    Redirect to the Dash app.

    """
    session['current_dataset'] = dataset
    return redirect('/plot/dataset')
