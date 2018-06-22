"""
    SpectraViewer.visualization.spectrum
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module contains things related to the visualization of spectra.

    :copyright: (c) 2018 by Iván Iglesias
    :license: license_name, see LICENSE for more details
"""
import dash_core_components as dcc
import dash_html_components as html
from flask import session

from SpectraViewer.visualization.common import get_processing_controls, \
    get_back_button, get_graph_help, get_controls_help


def compose_layout():
    """
    Compose and return the layout when visualizing a spectrum.

    Returns
    -------
    layout

    """
    from SpectraViewer.utils.mongo_facade import get_user_spectrum
    spectrum = session['current_spectrum']
    user_id = session['user_id']
    spectrum_data = get_user_spectrum(spectrum, user_id)
    layout = html.Div(children=[
        get_back_button(),
        html.Details(children=[
            html.Summary(className='btn btn-default', children='Ayuda'),
            html.Div(className='row', children=[
                html.Div(className='col-md-6', children=[
                    get_controls_help()
                ]),
                html.Div(className='col-md-6', children=[
                    get_graph_help()
                ])
            ])
        ]),
        html.H3(f'Espectro {spectrum}'),
        html.Div(className='row', children=[
            get_processing_controls(),
            html.Div(className='col-md-8', children=[
                dcc.Graph(
                    id='spectrum-original',
                    figure={
                        'layout': {
                            'title': 'Espectro original',
                            'xaxis': {'title': 'Raman shift'},
                            'yaxis': {'title': 'Intensity'}
                        },
                        'data': [{
                            'x': spectrum_data.columns.tolist(),
                            'y': spectrum_data.values[0],
                            'name': f'{spectrum}'
                        }]
                    },
                )
            ])
        ]),
        html.Div(className='row', children=[
            html.Div(className='col-md-12', children=[
                dcc.Graph(
                    id='spectrum-processed'
                )
            ])
        ])
    ])
    return layout
