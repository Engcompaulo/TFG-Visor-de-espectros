import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
from flask import session


def compose_layout():
    from SpectraViewer.utils.mongo_facade import get_user_dataset
    dataset = session['current_dataset']
    user_id = session['user_id']
    dataset_data = get_user_dataset(dataset, user_id)
    metadata = dataset_data.loc[:,
               ['Name', 'Label', 'Mina', 'Profundidad', 'Profundidad_num']]
    layout = html.Div(children=[
        html.A(className='btn btn-default', href='/manage',
               children=['Volver a mis archivos']),
        html.Div(className='page-header', children=[
            html.H2(f'Visualización del dataset {dataset}')
        ]),

        dt.DataTable(
            rows=metadata.to_dict('records'),
            row_selectable=True,
            filterable=True,
            sortable=True,
            selected_row_indices=[],
            id='metadata'

        ),
        html.Div(className='row', children=[
            html.Div(className='col-md-6', children=[
                dcc.Dropdown(
                    id='class_dropdown',
                    placeholder='Selecciona un conjunto de espectros',
                    options=[{'label': label, 'value': label} for label in
                             dataset_data['Label'].unique().tolist()],
                    clearable=False
                )
            ]),
            html.Div(className='col-md-6', children=[
                dcc.Dropdown(
                    id='class_data',
                    options=[],
                    placeholder='Selecciona un ejemplo del conjunto',
                    clearable=False
                )
            ])
        ]),
        dcc.Graph(
            id='spectrum'
        )
    ])

    return layout
