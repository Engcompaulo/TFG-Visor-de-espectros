"""
    SpectraViewer.visualization
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module contains all necessary things to manipulate the
    visualization of the graphs.

    :copyright: (c) 2018 by Iván Iglesias
    :license: license_name, see LICENSE for more details
"""
from flask import session, abort
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
from dash.dependencies import Input, Output

import numpy as np

from SpectraViewer.processing.Preprocess import preprocess_pipeline

_instance = None


def create_dash_app(server):
    """
    Create the Dash app and initialize it.

    Parameters
    ----------
    server : Flask
        Flask instance

    """
    global _instance
    app = dash.Dash(__name__, server=server, url_base_pathname='/plot/')
    app.config.suppress_callback_exceptions = True

    app.layout = html.Div(children=[
        html.Div(className='container-fluid', children=[
            dcc.Location(id='url', refresh=False),
            html.Div(id='page-content'),
            html.Div(dt.DataTable(rows=[{}]), style={'display': 'none'})
            # This is because of how Dash works
            # (see https://community.plot.ly/t/display-tables-in-dash/4707/40)
        ])
    ])
    app.css.append_css({
        'external_url': 'https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/css/bootstrap.min.css'})

    app.scripts.append_script({'external_url': [
        'https://cdnjs.cloudflare.com/ajax/libs/jquery/1.12.4/jquery.min.js',
        'https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/js/bootstrap.min.js']})

    _add_callbacks(app)

    _instance = app


def _add_callbacks(app):
    """
    Add the necessary callbacks to the Dash app.

    Parameters
    ----------
    app : Dash
        Dash app.

    """

    @app.callback(Output('page-content', 'children'),
                  [Input('url', 'pathname')])
    def display_page(pathname):
        """
        Returns the layout for the current path of the Dash application.

        Parameters
        ----------
        pathname : str
            Current path of the app.

        Returns
        -------
        layout

        """
        if pathname == '/plot/dataset':
            from SpectraViewer.visualization import dataset
            return dataset.compose_layout()
        elif pathname == '/plot/spectrum':
            from SpectraViewer.visualization import spectrum
            return spectrum.compose_layout()
        else:
            abort(404)

    @app.callback(Output('spectrum-original', 'figure'),
                  [Input('metadata', 'rows'),
                   Input('metadata', 'selected_row_indices')])
    def update_spectrum(rows, spectra_index):
        """
        Updates the spectrum graph with the new selected rows.

        Parameters
        ----------
        rows : list of dict
            Current rows in the table.
        spectra_index :  list
            Rows currently selected.

        Returns
        -------
        figure : dict
            Updated figure.

        """
        from SpectraViewer.utils.mongo_facade import get_user_dataset
        dataset = session['current_dataset']
        user_id = session['user_id']
        dataset_data = get_user_dataset(dataset, user_id)
        figure = {
            'layout': {
                'title': 'Espectro original',
                'xaxis': {'title': 'Raman shift'},
                'yaxis': {'title': 'Intensity'}
            },
            'data': list()
        }
        for i in spectra_index:
            name = rows[i]['Nombre']
            spectrum = dataset_data[dataset_data['Nombre'] == name]
            spectrum = spectrum.drop(
                columns=['Nombre', 'Etiqueta', 'Mina', 'Profundidad',
                         'Profundidad_num'])
            figure['data'].append({
                'x': spectrum.columns.tolist(),
                'y': spectrum.values[0],
                'name': f'{name}'
            })
        return figure

    @app.callback(Output('spectrum-processed', 'figure'),
                  [Input('spectrum-original', 'figure'),
                   Input('order', 'value'),
                   Input('crop-min', 'value'),
                   Input('crop-max', 'value'),
                   Input('baseline', 'value'),
                   Input('normalize', 'value'),
                   Input('squash', 'value'),
                   Input('smooth-type', 'value'),
                   Input('smooth-s', 'value')])
    def process_spectrum(figure, order, crop_min, crop_max, baseline, normalize,
                         squash, smooth_type, smooth_s):
        """
        Process the original spectra and return it as a figure for the
        processed spectrum graph.

        Parameters
        ----------
        figure : dict
            Figure of the original spectreum.
        order : str
            Processing order.
        crop_min : int
            Crop lower limit.
        crop_max : int
            Crop upper limit.
        baseline : str
            Baseline type.
        normalize : str
            Nomalization type.
        squash : str
            Squash type.
        smooth_type : str
            Smooth type.
        smooth_s : int
            Smooth size.

        Returns
        -------
        dict
            Processed figure.

        """
        processed_figure = figure
        processed_figure['layout']['title'] = 'Espectro procesado'
        old_data = figure['data']
        new_data = list()
        for spectrum in old_data:
            values = spectrum['y']
            size = len(values)
            X, atts = preprocess_pipeline(np.array(values).reshape((1, size)),
                                          spectrum['x'],
                                          order, crop_min, crop_max, baseline,
                                          normalize, squash, smooth_type,
                                          smooth_s)
            new_values = X[0].tolist()
            new_data.append(
                {'x': atts, 'y': new_values, 'name': spectrum['name']})

        processed_figure['data'] = new_data
        return processed_figure
