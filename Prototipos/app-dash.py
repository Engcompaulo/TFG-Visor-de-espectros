from flask import Flask, render_template, url_for, redirect
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import cufflinks as cf

class CsvForm(FlaskForm):
    file = FileField(validators=[FileRequired(), FileAllowed(['csv'], 'Solo ficheros .csv')])

server = Flask(__name__)

server.config['SECRET_KEY'] = 'secret key'

app = dash.Dash(__name__, server=server, url_base_pathname='/dash_app')
app.title = 'Aplicación Dash'
app.layout = html.Div()

cf.go_offline()

@server.route('/')
@server.route('/index')
def index():
    return render_template('index-dash.html')


@server.route('/upload', methods=['GET', 'POST'])
def upload():
    form = CsvForm()
    if form.validate_on_submit():
        f = form.file.data
        filename = secure_filename(f.filename)
        f.save(os.path.join('csvs', filename))
        data = pd.read_csv('{}/{}'.format('csvs',filename), sep=';', header=None)
        data.columns = ['longitud','valor']
        fig = data.iplot(x='longitud', y='valor', kind='scatter', asFigure=True, title='Datos de ejemplo', xTitle='Longitud de onda', yTitle='Valor')
        app.layout = html.Div([
            html.H1('Aplicación Dash'),

            dcc.Graph(
                id='example-graph',
                figure=fig
            )
        ])
        return redirect('/dash_app')
    return render_template('upload.html', form=form)



if __name__ == '__main__':
    server.run(debug=True)