import dash_core_components as dcc
import dash_html_components as html
from flask import session

from SpectraViewer.utils.directories import get_dataset_data


def compose_layout():
    dataset = session['current_dataset']
    dataset_data = get_dataset_data(dataset)
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
                             class_name in dataset_data],
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
