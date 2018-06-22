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

import pickle

from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression, RidgeClassifier
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, \
    GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import LinearSVC

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from SpectraViewer.main import main
from SpectraViewer.main.forms import SpectrumForm, DatasetForm, ClassifierForm
from SpectraViewer.utils.decorators import google_required
from SpectraViewer.processing.Preprocess import preprocess_pipeline
from SpectraViewer.utils.mongo_facade import *
from SpectraViewer.utils.directories import get_temp_directory, get_path, \
    get_user_directory

_available_models = {'LDA': LinearDiscriminantAnalysis,
                     'Knn': KNeighborsClassifier,
                     'LR': LogisticRegression,
                     'Ridge': RidgeClassifier,
                     'RF': RandomForestClassifier,
                     'Extra': ExtraTreesClassifier,
                     'GBT': GradientBoostingClassifier,
                     'Tree': DecisionTreeClassifier,
                     'SVM': LinearSVC}


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
    user_classifiers = get_classifiers(user_id)
    return render_template('manage.html', datasets=user_datasets,
                           spectra=user_spectra, classifiers=user_classifiers)


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
    the file and saves it to mongo.

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


@main.route('/create-model/<dataset>')
@google_required
def create_model(dataset):
    """Render the create model view.

    A dropdown with the supported models is displayed, then the model
    parameters are shown when selected.

    Parameters
    ----------
    dataset : str
        Dataset to be used when training the model.

    """
    models = {model_id: model.__name__ for model_id, model in
              _available_models.items()}
    return render_template('create_model.html', models=models, dataset=dataset)


@main.route('/train-model/<dataset>', methods=['POST'])
@google_required
def train_model(dataset):
    """Train the selected model with the desired parameters.

    Train the model, calculate scores and save it, then redirect to
    the manage view, displaying a message with the classifier scores.

    Parameters
    ----------
    dataset : str
        Dataset to be used when training the model.

    """
    parameters = {}
    for param, value in request.form.items():
        if value == 'True':
            parameters[param] = True
        elif value == 'False':
            parameters[param] = False
        elif value != '':  # Numbers and strings
            try:
                parameters[param] = int(value)
            except ValueError:
                try:
                    parameters[param] = float(value)
                except ValueError:
                    parameters[param] = value
    model = _available_models[session['model']]
    data = get_user_dataset(dataset, session['user_id'])
    y_mine = data['Mina'].values.astype(str)
    y_prof = data['Profundidad'].values.astype(str)
    y_prof_num = data['Profundidad_num'].values.astype(str)
    x = data.drop(columns=['Nombre', 'Etiqueta', 'Mina', 'Profundidad',
                           'Profundidad_num'])
    x_pro, _ = preprocess_pipeline(x.values, x.columns, 'sCBN', 50, 1800,
                                   'ALS_old', 'norm', 'cos', 'sg', 25)
    test_size = 0.3
    x_mine_train, x_mine_test, y_mine_train, y_mine_test = train_test_split(
        x_pro, y_mine, test_size=test_size)
    x_prof_train, x_prof_test, y_prof_train, y_prof_test = train_test_split(
        x_pro, y_prof, test_size=test_size)
    x_pnum_train, x_pnum_test, y_pnum_train, y_pnum_test = train_test_split(
        x_pro, y_prof_num, test_size=test_size)
    try:
        mine_classifier = model(**parameters).fit(x_mine_train, y_mine_train)
        mine_accuracy = accuracy_score(y_mine_test,
                                       mine_classifier.predict(x_mine_test))
        prof_classifier = model(**parameters).fit(x_prof_train, y_prof_train)
        prof_accuracy = accuracy_score(y_prof_test,
                                       prof_classifier.predict(x_prof_test))
        pnum_classifier = model(**parameters).fit(x_pnum_train, y_pnum_train)
        pnum_accuracy = accuracy_score(y_pnum_test,
                                       pnum_classifier.predict(x_pnum_test))
        classifiers = ClassifierSet(None, session['user_id'], None,
                                    mine_classifier, prof_classifier,
                                    pnum_classifier)
        temp = get_path(get_user_directory(), 'classifiers.pk')
        with open(temp, 'wb') as temp_file:
            pickle.dump(classifiers, temp_file)
        session['results'] = {'mine': format(mine_accuracy * 100, '.2f'),
                              'prof': format(prof_accuracy * 100, '.2f'),
                              'pnum': format(pnum_accuracy * 100, '.2f')}
    except Exception as e:
        flash(str(e), 'danger')
        return redirect(url_for('main.create_model', dataset=dataset))
    else:
        return redirect(url_for('main.results'))


@main.route('/results', methods=['GET', 'POST'])
@google_required
def results():
    """
    Shows the test results and presents a form for saving the classifiers.

    """
    test_results = session['results']
    form = ClassifierForm()
    if form.validate_on_submit():
        temp = get_path(get_user_directory(), 'classifiers.pk')
        with open(temp, 'rb') as temp_file:
            classifiers = pickle.load(temp_file)
        classifiers.name = form.name.data
        classifiers.notes = form.notes.data
        if save_classifiers(classifiers):
            flash('Clasificador guardado correctamente', 'success')
            return redirect(url_for('main.manage'))
        else:
            flash('Clasificador ya existente', 'danger')
            return redirect(url_for('main.results'))
    form.name.data = _available_models[session['model']].__name__
    form.notes.data = f"Mina: {test_results['mine']}% acierto, " \
                      f"Profundidad: {test_results['prof']}% acierto, " \
                      f"Profundidad_num: {test_results['pnum']}% acierto. "
    return render_template('results.html', results=test_results,
                           form=form)


@main.route('/model-parameters/<model_key>')
@google_required
def model_params(model_key):
    """Return a custom form with the parameters of the given model.

    Parameters
    ----------
    model_key : Key of the model stored in available models.

    Returns
    -------
    Custom form.

    """
    doc = ClassDoc(_available_models[model_key])
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
    session['model'] = model_key
    return render_template('model_parameters.html', params=params)


@main.route('/delete_classifier/<classifier>')
@google_required
def delete_classifier(classifier):
    """
    Remove the classifiers object with the given name from the database.

    Parameters
    ----------
    classifier : str
        Classifires object name.

    Returns
    -------
    Redirect to the manage view.

    """
    remove_classifiers(classifier, session['user_id'])
    flash('Se ha borrado correctamente el clasificador', 'success')
    return redirect(url_for('main.manage'))


@main.route('/predict/<spectrum>', methods=['GET', 'POST'])
@google_required
def predict(spectrum):
    classifiers = get_classifiers(session['user_id'])
    if request.method == 'POST':
        selected = request.form['classifier-select']
        data = get_user_spectrum(spectrum, session['user_id'])
        x_pro, _ = preprocess_pipeline(data.values, data.columns, 'sCBN', 50,
                                       1800, 'ALS_old', 'norm', 'cos', 'sg', 25)
        classifier = get_classifier(selected, session['user_id'])
        predictions = dict()
        predictions['mine'] = classifier.mine.predict(x_pro)[0]
        predictions['prof'] = classifier.prof.predict(x_pro)[0]
        predictions['pnum'] = classifier.pnum.predict(x_pro)[0]
        return render_template('predict.html', classifiers=classifiers,
                               predictions=predictions, spectrum=spectrum)
    return render_template('predict.html', classifiers=classifiers,
                           predictions=None, spectrum=spectrum)
