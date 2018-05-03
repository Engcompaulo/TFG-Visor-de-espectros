import dash_core_components as dcc
import dash_html_components as html
from flask import session


def compose_layout():
    from SpectraViewer.utils.mongo_facade import get_user_dataset
    dataset = session['current_dataset']
    user_id = session['user_id']
    dataset_data = get_user_dataset(dataset, user_id)
    layout = html.Div(children=[
        html.A(className='btn btn-default', href='/manage',
               children=['Volver a mis archivos']),
        html.Div(className='page-header', children=[
            html.H2(f'Visualización del dataset {dataset}')
        ]),
        html.Div(className='row', children=[
            html.Div(className='col-md-6', children=[
                dcc.Dropdown(
                    id='class_dropdown',
                    placeholder='Selecciona una clase',
                    options=[{'label': class_name, 'value': class_name} for
                             class_name in dataset_data.keys()],
                    clearable=False
                )
            ]),
            html.Div(className='col-md-6', children=[
                dcc.Dropdown(
                    id='class_data',
                    options=[],
                    placeholder='Selecciona un espectro',
                    clearable=False
                )
            ])
        ]),
        dcc.Graph(
            id='spectrum'
        )
    ])

    return layout
