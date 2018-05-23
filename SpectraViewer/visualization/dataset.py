"""
    SpectraViewer.visualization.dataset
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module contains things related to the visualization of datasets.

    :copyright: (c) 2018 by Iván Iglesias
    :license: license_name, see LICENSE for more details
"""
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
from flask import session

from SpectraViewer.processing.Preprocess import PreprocessOperator


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
    prep = PreprocessOperator('normalize', type='norm')
    prep_options = prep.get_options()
    norm_options = prep_options['normalize']['type']
    squash_options = prep_options['squash']['type']
    smooth_options = prep_options['smooth']['type']
    crop_min = prep_options['crop']['orig'][0]
    crop_max = prep_options['crop']['orig'][1]
    baselines = ['ALS_old', 'airpls', 'als', 'fabc', 'median', 'mpls', 'tophat']
    layout = html.Div(children=[
        html.A(className='btn btn-default', href='/manage',
               children=['Volver a mis archivos']),
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
            html.Div(className='col-md-4', children=[
                html.Div(className='form-horizontal', children=[
                    html.Div(className='form-group', children=[
                        html.Label(htmlFor='order',
                                   className='col-md-4 control-label',
                                   children='Orden de procesado'),
                        html.Div(className='col-md-8', children=[
                            dcc.Input(
                                id='order',
                                className='form-control',
                                placeholder='Introduce el orden de procesado',
                                type='text',
                                value='sCBN'
                            )
                        ])
                    ]),
                    html.Div(className='form-group', children=[
                        html.Label(htmlFor='crop-min',
                                   className='col-md-4 control-label',
                                   children='Recorte (min, max) (C)'),
                        html.Div(className='col-md-4', children=[
                            dcc.Input(
                                id='crop-min',
                                min=crop_min,
                                max=crop_max,
                                className='form-control',
                                placeholder=50,
                                type='number',
                                value=50
                            )
                        ]),
                        html.Div(className='col-md-4', children=[
                            dcc.Input(
                                id='crop-max',
                                min=crop_min,
                                max=crop_max,
                                className='form-control',
                                placeholder=2800,
                                type='number',
                                value=1800
                            )
                        ])
                    ]),
                    html.Div(className='form-group', children=[
                        html.Label(htmlFor='baseline',
                                   className='col-md-4 control-label',
                                   children='Línea base (B)'),
                        html.Div(className='col-md-8', children=[
                            dcc.Dropdown(options=[
                                {'label': baseline, 'value': baseline}
                                for baseline in baselines
                            ], value='ALS_old', searchable=False,
                                clearable=False, id='baseline')
                        ])
                    ]),
                    html.Div(className='form-group', children=[
                        html.Label(htmlFor='normalize',
                                   className='col-md-4 control-label',
                                   children='Normalización (N)'),
                        html.Div(className='col-md-8', children=[
                            dcc.Dropdown(options=[
                                {'label': norm_option, 'value': norm_option}
                                for norm_option in norm_options
                            ], value='norm',
                                searchable=False, clearable=False,
                                id='normalize')
                        ])
                    ]),
                    html.Div(className='form-group', children=[
                        html.Label(htmlFor='squash',
                                   className='col-md-4 control-label',
                                   children='Aplastado (S)'),
                        html.Div(className='col-md-8', children=[
                            dcc.Dropdown(options=[
                                {'label': squash_option, 'value': squash_option}
                                for squash_option in squash_options
                            ], value='sqrt',
                                searchable=False, clearable=False,
                                id='squash')
                        ])
                    ]),
                    html.Div(className='form-group', children=[
                        html.Label(htmlFor='smooth-type',
                                   className='col-md-4 control-label',
                                   children='Tipo de suavizado (s)'),
                        html.Div(className='col-md-8', children=[
                            dcc.Dropdown(options=[
                                {'label': smooth_option, 'value': smooth_option}
                                for smooth_option in smooth_options
                            ], value='sg',
                                searchable=False, clearable=False,
                                id='smooth-type')
                        ])
                    ]),
                    html.Div(className='form-group', children=[
                        html.Label(htmlFor='smooth-s',
                                   className='col-md-4 control-label',
                                   children='Ventana de suavizado'),
                        html.Div(className='col-md-8', children=[
                            dcc.Slider(
                                id='smooth-s',
                                min=3,
                                max=35,
                                marks={i: i for i in range(3, 36, 2)},
                                value=25,
                            ),
                        ])
                    ])

                ]),
            ])
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
