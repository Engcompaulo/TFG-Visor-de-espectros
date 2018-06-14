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
from numpydoc.docscrape import ClassDoc
from sklearn.linear_model import LogisticRegression, LinearRegression

from SpectraViewer.main import main
from SpectraViewer.main.forms import SpectrumForm, DatasetForm
from SpectraViewer.utils.decorators import google_required
from SpectraViewer.utils.mongo_facade import save_dataset, remove_dataset, \
    get_datasets, save_spectrum, get_spectra, remove_spectrum, get_user_dataset
from SpectraViewer.utils.directories import get_temp_directory, get_path, \
    get_user_directory

_available_models = {'logistic': LogisticRegression,
                     'linear': LinearRegression}


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
    user_datasets = [{'name': dataset.name,
                      'notes': dataset.notes} for dataset in
                     get_datasets(user_id)]
    user_spectra = [{'name': spectrum.name,
                     'notes': spectrum.notes} for spectrum in
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


@main.route('/spectrum/plot/<spectrum>')
@google_required
def plot_spectrum(spectrum):
    """
    Redirect the user to the visualization page with the given spectrum.

    Parameters
    ----------
    spectrum : str
        Spectrum name.

    Returns
    -------
    Redirect to the Dash app.

    """
    session['current_spectrum'] = spectrum
    return redirect('/plot/spectrum')


@main.route('/create-model/<dataset>', methods=['GET', 'POST'])
@google_required
def create_model(dataset):
    if request.method == 'POST':
        parameters = {}
        for param, value in request.form.items():
            if value != '':
                if value == 'True':
                    parameters[param] = True
                elif value == 'False':
                    parameters[param] = False
                else:
                    parameters[param] = value  # Numbers and strings
        print(parameters)
        model = _available_models[session['model']](**parameters)
        data = get_user_dataset(dataset, session['user_id'])
        # y_mina = data['Mina']
        # y_prof = data['Profundidad']
        y_prof_num = data['Profundidad_num']
        x = data.drop(columns=['Nombre', 'Etiqueta', 'Mina', 'Profundidad',
                               'Profundidad_num'])
        # model_mina = model.fit(x, y_mina)
        # mode_prof = model.fit(x, y_prof)
        try:
            mode_prof_num = model.fit(x, y_prof_num)
        except Exception as e:
            print(e)
            flash(str(e), 'danger')
        return redirect(url_for('main.create_model', dataset=dataset))
    models = {model_id: model.__name__ for model_id, model in
              _available_models.items()}
    return render_template('create_model.html', models=models, dataset=dataset)


@main.route('/model-parameters/<model_id>')
@google_required
def model_params(model_id):
    doc = ClassDoc(_available_models[model_id])
    params = doc['Parameters']
    params = list(map(list, params))  # Because previous line returns tuples
    for param in params:
        # Returns a list with description, each element is a line
        description_list = param[2]
        try:
            break_index = description_list.index('')
        except ValueError:
            break_index = len(description_list)
        description = ' '.join(description_list[0:break_index])
        param[2] = description
    session['model'] = model_id
    return render_template('model_parameters.html', params=params)
