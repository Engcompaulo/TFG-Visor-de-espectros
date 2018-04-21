"""
    SpectraViewer.main.routes
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    This file contains the routes of the main module.

    :copyright: (c) 2018 by Iván Iglesias
    :license: license_name, see LICENSE for more details
"""
from flask import render_template, redirect, url_for, request, session, flash
from werkzeug.utils import secure_filename
from zipfile import ZipFile

# Importing cufflinks is required to able to get the plotly figure from
# a DataFrame, the import binds the DataFrame with the iplot method.
import pandas as pd
import cufflinks

from SpectraViewer.main import main
from SpectraViewer.main.forms import SpectrumForm, DatasetForm
from SpectraViewer.visualization.app import set_dash_layout, get_dash_app
from SpectraViewer.utils.decorators import google_required
from SpectraViewer.utils.directories import get_temp_directory, get_path, \
    get_user_datasets, get_user_spectra, get_user_directory


@main.before_request
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


@main.route('/upload', methods=['GET', 'POST'])
def upload():
    """Render for the upload view.

    This view contains a form for file uploading. If POST request,
    validates the selected file and saves it. Then pandas reads it and
    the Dash layout gets defined. Then redirect to the Dash route.

    Returns
    -------
    Rendered upload view if GET, redirect to Dash if POST

    """
    form = SpectrumForm()
    if form.validate_on_submit():
        f = form.file.data
        filename = secure_filename(f.filename)
        directory = get_temp_directory()
        file_path = get_path(directory, filename)
        f.save(file_path)
        data = pd.read_csv(file_path, sep=';', header=None)
        data.columns = ['Raman shift', 'Intensity']
        figure = data.iplot(x='Raman shift', y='Intensity', asFigure=True,
                            xTitle='Raman shift', yTitle='Intensity')
        set_dash_layout(figure, 'Visualización del espectro')
        return redirect(url_for('main.dash'))
    return render_template('upload.html', form=form)


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
    user_datasets = get_user_datasets()
    user_spectra = get_user_spectra()
    return render_template('manage.html', datasets=user_datasets,
                           spectra=user_spectra)


@main.route('/datasets/upload', methods=['GET', 'POST'])
@google_required
def upload_dataset():
    """Render the upload dataset view.

    This page contains a form for uploading datasets, contains
    instructions on how the zip should be composed. If POST, uploads the
    file and extracts it to the user directory with the name provided in
    the form.

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
        with ZipFile(file_path, 'r') as zip_file:
            zip_file.extractall(get_path(user_directory, form.name.data))
        flash('Se ha subido el dataset correctamente', 'success')
        return redirect(url_for('main.manage'))
    return render_template('upload_dataset.html', form=form)


@main.route('/datasets/edit/<dataset>')
@google_required
def edit_dataset(dataset):
    return 'Not yet implemented'


@main.route('/datasets/delete/<dataset>')
@google_required
def delete_dataset(dataset):
    flash('Se ha borrado correctamente el dataset')
    return redirect(url_for('main.manage'))


@main.route('/datasets/plot/<dataset>')
@google_required
def plot_dataset(dataset):
    dash_app = get_dash_app()
    dash_app.title = 'Visualización del dataset'
    session['current_dataset'] = dataset
    return redirect('/plot/dataset')


@main.route('/dash')
def dash():
    """Redirect to the Dash application.

    This route helps the use of url_for so it can be used everywhere in
    the app to get the url for Dash.
    """
    return redirect('/plot')
