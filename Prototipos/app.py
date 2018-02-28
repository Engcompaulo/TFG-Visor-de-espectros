from flask import Flask, render_template, url_for
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import cufflinks as cf

server = Flask(__name__)

server.config['SECRET_KEY'] = 'secret key'

app = dash.Dash(__name__, server=server, url_base_pathname='/dash_app')
app.title = 'Aplicación Dash'
cf.go_offline()
data = pd.read_csv('datos.csv', sep=',', header=None)
data.columns = ['x','y']
fig = data.iplot(x='x', y='y', asFigure=True, title='Datos de ejemplo')

@server.route('/')
@server.route('/index')
def index():
    return render_template('index-dash.html')

app.layout = html.Div(children=[
    html.H1(children='Aplicación Dash'),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])


if __name__ == '__main__':
    server.run(debug=True)