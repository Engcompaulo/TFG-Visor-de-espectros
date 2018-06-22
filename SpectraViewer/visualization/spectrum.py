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

from SpectraViewer.visualization.common import get_processing_controls


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
        html.A(className='btn btn-default', href='/manage',
               children=['Volver a mis archivos']),
        html.Details(children=[
            html.Summary(className='btn btn-default', children='Ayuda'),
            html.Div(className='row', children=[
                html.Div(className='col-md-6', children=[
                    html.Div(className='panel panel-default', children=[
                        html.Div(className='panel-heading',
                                 children=html.H4(
                                     'Controles de procesamiento')),
                        html.Div(className='panel-body', children=[
                            html.P(
                                'Cada etiqueta asociada a un control tiene entre paréntesis la letra que lo representa'),
                            html.P(
                                'En el cuadro "Orden de procesado" hay que introducir '
                                'las letras de los controles en el orden que se quiera realizar el procesado'),
                            html.Dl(className='dl-horizontal', children=[
                                html.Dt('Recorte'), html.Dd(
                                    'Muestra los valores entre el rango definido'),
                                html.Dt('Línea base'),
                                html.Dd('Elimina la línea base del gráfico'),
                                html.Dt('Normalización'),
                                html.Dd('Normaliza los valores de los datos'),
                                html.Dt('Aplastado'),
                                html.Dd('Aplasta los valores de los datos'),
                                html.Dt('Suavizado'),
                                html.Dd('Elimina pequeños picos en los datos, '
                                        'se requiere escoger un tipo y un tamaño, '
                                        'cuanto mayor sea el tamaño menos picos quedan'),

                            ])
                        ])
                    ])
                ]),
                html.Div(className='col-md-6', children=[
                    html.Div(className='panel panel-default', children=[
                        html.Div(className='panel-heading',
                                 children=html.H4('Opciones de los gráficos')),
                        html.Div(className='panel-body', children=[
                            html.Ul(children=[
                                html.Li(
                                    'Seleccionando una zona sobre el gráfico se hace zoom en esa parte'),
                                html.Li(
                                    'Haciendo doble click después de hacer zoom se vuelve a la vista general'),
                                html.P('Con varios ejemplos seleccionados:'),
                                html.Ul(children=[
                                    html.Li(
                                        'Haciendo click en el nombre de uno se oculta del gŕafico'),
                                    html.Li(
                                        'Haciendo doble click en el nombre de uno se ocultan el resto'),
                                ]),
                                html.Li(
                                    'El propio gráfico tiene que varias cuya función se muestra al pasar el ratón por encima de su icono')
                            ])
                        ])
                    ])
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
