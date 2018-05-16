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
        html.A(className='btn btn-default', href='/manage',
               children=['Volver a mis archivos']),
        html.H3(f'Dataset {dataset}'),
        dt.DataTable(
            rows=metadata.to_dict('records'),
            row_selectable=True,
            filterable=True,
            sortable=True,
            editable=False,
            selected_row_indices=[],
            max_rows_in_viewport=5,
            id='metadata'
        ),
        dcc.Graph(
            id='spectrum-original'
        )
    ])

    return layout
