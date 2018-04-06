"""
    SpectraViewer.routes
    ~~~~~~~~~~~~~~~~~~~

    This file contains the routes of the application.

    :copyright: (c) 2018 by Iván Iglesias
    :license: license_name, see LICENSE for more details
"""
import os

from flask import render_template, redirect, url_for, request, session
from werkzeug.utils import secure_filename

import dash_core_components as dcc
import dash_html_components as html

from flask_dance.contrib.google import google

# Importing cufflinks is required to able to get the plotly figure from
# a DataFrame, the import binds the DataFrame with the iplot method.
import pandas as pd
import cufflinks as cf

from SpectraViewer.app import server, app
from SpectraViewer.forms import CsvForm
from SpectraViewer.decorators import google_required


@server.before_request
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


@server.route('/')
@server.route('/index')
def index():
    """Render the index view.

    Welcome or index page of this web app.
    """
    email = None
    if google.authorized:
        email = session['email']
    return render_template('index.html', email=email)


@server.route('/upload', methods=['GET', 'POST'])
@google_required
def upload():
    """Render for the upload view.

    This view contains a form for file uploading. If POST request,
    validates the selected file and saves it. Then pandas reads it and
    the Dash layout gets defined. The redirect to the Dash route.
    """
    form = CsvForm()
    if form.validate_on_submit():
        f = form.file.data
        filename = secure_filename(f.filename)
        directory = os.path.join(server.instance_path,
                                 server.config['UPLOAD_FOLDER'],
                                 session['email'])
        if not os.path.exists(directory):
            os.makedirs(directory)
        f.save(os.path.join(directory, filename))
        data = pd.read_csv(f'{directory}/{filename}', sep=';', header=None)
        data.columns = ['Raman shift', 'Intensity']
        figure = data.iplot(x='Raman shift', y='Intensity', asFigure=True,
                            xTitle='Raman shift', yTitle='Intensity'
                            )
        add_external_resources()
        app.layout = get_dash_layout(figure)
        return redirect(url_for('dash'))
    return render_template('upload.html', form=form, email=session['email'])


@server.route('/dash')
@google_required
def dash():
    """Redirect to the dash application.

    This route allows the use of url_for() for the dash application.
    """
    return redirect('/plot')


def add_external_resources():
    app.css.append_css({
        'external_url': 'http://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/css/bootstrap.min.css'})

    app.scripts.append_script({'external_url': [
        'http://cdnjs.cloudflare.com/ajax/libs/jquery/1.12.4/jquery.min.js',
        'http://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/js/bootstrap.min.js']})


def get_dash_layout(figure):
    """
    Build and return the layout for the dash application.

    Receives the figure returned by the iplot() method and returns the
    layout of the dash application with that figure.

    Parameters
    ----------
    figure
        The figure which will be represented.

    Returns
    -------
    Div
        The Div to assign to the dash application layout.
    """
    app.title = 'Visualización del espectro'
    back = html.A(className='btn btn-default', href='/index', children=[
        'Volver a la página principal'
    ])
    # navbar = html.Nav(className='navbar navbar-inverse', children=[
    #     html.Div(className='container', children=[
    #         html.Div(className='navbar-header', children=[
    #             html.Button(type='button', className='navbar-toggle',
    #                         dataToggle='collapse',
    #                         dataTarget='.navbar-collapse', children=[
    #                     html.Span(className='sr-only',
    #                               children='Toggle navigation'),
    #                     html.Span(className='icon-bar'),
    #                     html.Span(className='icon-bar'),
    #                     html.Span(className='icon-bar')
    #                 ]),
    #             html.Span(className='navbar-brand',
    #                       children='Visor de espectros')
    #         ]),
    #         html.Div(className='collapse navbar-collapse', children=[
    #             html.Ul(className='nav navbar-nav', children=[
    #                 html.Li(html.A('Inicio', href=url_for('index'))),
    #                 html.Li(html.A('Subir espectro', href=url_for('upload')))
    #             ]),
    #             html.Ul(className='nav navbar-nav navbar-right', children=[
    #                 html.Li(html.A('Iniciar Sesión', href=""))
    #             ])
    #         ])
    #     ])
    # ])
    content = html.Div(className='container', children=[
        html.Div(className='page-header', children=[
            html.H2('Representación del espectro')
        ])
    ])
    return html.Div([
        back,
        content,
        dcc.Graph(
            id='example-graph',
            figure=figure
        )
    ])
