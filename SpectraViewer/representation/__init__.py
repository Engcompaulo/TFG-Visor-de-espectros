"""
    SpectraViewer.representation
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module contains all necessary things to manipulate the
    representation of the graphs.

    :copyright: (c) 2018 by Iván Iglesias
    :license: license_name, see LICENSE for more details
"""
from flask import url_for
import dash
import dash_core_components as dcc
import dash_html_components as html

_instance = None


def get_dash_app():
    """
    Get the Dash app instance.

    Returns
    -------
    Dash
        An instance if exists, None otherwise.

    """
    return _instance


def create_dash_app(server):
    """
    Create the Dash app and initialize it.

    Parameters
    ----------
    server : Flask
        Flask instance

    """
    global _instance
    app = dash.Dash(__name__, server=server, url_base_pathname='/plot')
    app.layout = html.Div()
    app.css.append_css({
            'external_url': 'https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/css/bootstrap.min.css'})

    app.scripts.append_script({'external_url': [
        'https://cdnjs.cloudflare.com/ajax/libs/jquery/1.12.4/jquery.min.js',
        'https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/js/bootstrap.min.js']})

    _instance = app


def set_dash_layout(figure, title):
    """
    Build and set the layout for the Dash application.

    Receives the figure returned by the iplot() method and returns the
    layout of the Dash application with that figure.

    Parameters
    ----------
    figure : plotly Figure
        The figure which will be represented.
    title : str
        Title of the web page.

    """
    app = get_dash_app()
    app.title = title
    back = html.A(className='btn btn-default', href=url_for('main.index'),
                  children=[
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
    #                 html.Li(html.A('Inicio', href=url_for('main.index'))),
    #                 html.Li(html.A('Subir espectro', href=url_for('main.upload')))
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
    app.layout = html.Div([
        back,
        content,
        dcc.Graph(
            id='graph',
            figure=figure
        )
    ])
