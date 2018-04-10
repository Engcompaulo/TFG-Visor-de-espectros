"""
    SpectraViewer.main.routes
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    This file contains the routes of the main module.

    :copyright: (c) 2018 by Iván Iglesias
    :license: license_name, see LICENSE for more details
"""
import os

from flask import render_template, redirect, url_for, request, session, \
    current_app
from werkzeug.utils import secure_filename

from flask_dance.contrib.google import google

# Importing cufflinks is required to able to get the plotly figure from
# a DataFrame, the import binds the DataFrame with the iplot method.
import pandas as pd
import cufflinks

from SpectraViewer.main import main
from SpectraViewer.main.forms import CsvForm
from SpectraViewer.representation import set_dash_layout
from SpectraViewer.utils.decorators import google_required


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
    email = None
    if google.authorized:
        email = session['email']
    return render_template('index.html', email=email)


@main.route('/upload', methods=['GET', 'POST'])
@google_required
def upload():
    """Render for the upload view.

    This view contains a form for file uploading. If POST request,
    validates the selected file and saves it. Then pandas reads it and
    the Dash layout gets defined. Then redirect to the Dash route.

    Returns
    -------
    Rendered upload view if GET, redirect to Dash if POST

    """
    form = CsvForm()
    email = session['email']
    if form.validate_on_submit():
        f = form.file.data
        filename = secure_filename(f.filename)
        directory = os.path.join(current_app.instance_path,
                                 current_app.config['UPLOAD_FOLDER'],
                                 email)
        if not os.path.exists(directory):
            os.makedirs(directory)
        f.save(os.path.join(directory, filename))
        data = pd.read_csv(f'{directory}/{filename}', sep=';', header=None)
        data.columns = ['Raman shift', 'Intensity']
        figure = data.iplot(x='Raman shift', y='Intensity', asFigure=True,
                            xTitle='Raman shift', yTitle='Intensity'
                            )
        set_dash_layout(figure, 'Visualización del espectro')
        return redirect(url_for('main.dash'))
    return render_template('upload.html', form=form, email=email)


@main.route('/dash')
@google_required
def dash():
    """Redirect to the Dash application.

    This route helps the use of url_for so it can be used everywhere in
    the app to get the url for Dash.
    """
    return redirect('/plot')