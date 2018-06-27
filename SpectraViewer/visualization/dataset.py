"""
    SpectraViewer.visualization.dataset
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module contains things related to the visualization of datasets.

    :copyright: (c) 2018 by Iván Iglesias
    :license: GPL-3.0, see LICENSE for more details
"""
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
from flask import session

from SpectraViewer.visualization.common import get_processing_controls, \
    get_back_button, get_graph_help, get_controls_help


def compose_layout():
    """
    Compose and return the layout when visualizing a dataset.

    Returns
    -------
    layout

    """
    from SpectraViewer.utils.mongo_facade import get_user_dataset
    dataset = session['current_dataset']
    user_id = session['user_id']
    dataset_data = get_user_dataset(dataset, user_id)
    metadata = dataset_data.loc[:, ['Nombre', 'Etiqueta', 'Mina', 'Profundidad',
                                    'Profundidad_num']]
    layout = html.Div(children=[
        get_back_button(),
        html.Details(children=[
            html.Summary(className='btn btn-default', children='Ayuda'),
            html.Div(className='row', children=[
                html.Div(className='col-md-4', children=[
                    html.Div(className='panel panel-default', children=[
                        html.Div(className='panel-heading',
                                 children=html.H4('Tabla de datos')),
                        html.Div(className='panel-body', children=[
                            html.Ul(children=[
                                html.Li(
                                    'Seleccione en la tabla los ejemplos que quiera representar'),
                                html.Li(
                                    'Se pueden seleccionar varios ejemplos a la vez'),
                                html.Li(
                                    'Pulsando el botón "Filter Rows" aparcen unas cajas de texto en cada columna para filtrar las filas por ese valor'),
                                html.Li(
                                    'Pulsando en el nombre de la columna, se ordena de forma ascendente o descendente')
                            ])
                        ])
                    ])
                ]),
                html.Div(className='col-md-4', children=[
                    get_controls_help()
                ]),
                html.Div(className='col-md-4', children=[
                    get_graph_help()
                ])
            ])
        ])
        ,
        html.H3(f'Dataset {dataset}'),
        html.Div(className='row', children=[
            html.Div(className='col-md-8', children=[
                dt.DataTable(
                    rows=metadata.to_dict('records'),
                    row_selectable=True,
                    filterable=True,
                    sortable=True,
                    editable=False,
                    selected_row_indices=[],
                    max_rows_in_viewport=6,
                    id='metadata'
                )
            ]),
            get_processing_controls()
        ]),
        html.Div(className='row', children=[
            html.Div(className='col-md-6', children=[
                dcc.Graph(
                    id='spectrum-original'
                )
            ]),
            html.Div(className='col-md-6', children=[
                dcc.Graph(
                    id='spectrum-processed'
                )
            ])
        ])
    ])

    return layout
