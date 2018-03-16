"""
    SpectraViewer.app
    ~~~~~~~~~~~~~~~~~

    This is just a prototype for the full application. Right now all
    code is contained in this file, this is intended to change in the
    future.

    :copyright: (c) 2018 by Iván Iglesias
    :license: license_name, see LICENSE for more details
"""
from flask import Flask, render_template, redirect
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
    """Form for handling file upload.

        Attributes
        ----------
        file : FileField
            Allows the user to upload a file to the server. Only .csv
            files are allowed.
        """
    file = FileField(validators=[FileRequired(),
                                 FileAllowed(['csv'], 'Solo ficheros .csv')])


server = Flask(__name__)

server.config['SECRET_KEY'] = 'secret key'
server.config['UPLOAD_FOLDER'] = 'csvs'

app = dash.Dash(__name__, server=server, url_base_pathname='/dash_app')
app.title = 'Aplicación Dash'
app.layout = html.Div()  # Needs a layout, so empty layout is good to go

cf.go_offline()


@server.route('/')
@server.route('/index')
def index():
    """Render the index view.

    Welcome or index page of this web app.
    """
    return render_template('index-dash.html')


@server.route('/upload', methods=['GET', 'POST'])
def upload():
    """Render for the upload view.

    This view contains a form for file uploading. If POST request,
    validates the selected file and saves it. Then pandas reads it and
    the Dash layout gets defined. The redirect to the Dash route.
    """
    form = CsvForm()
    if form.validate_on_submit():
        f = form.file.data
        filename = secure_filename(f.filename)
        directory = os.path.join(server.instance_path,
                                 server.config['UPLOAD_FOLDER'])
        if not os.path.exists(directory):
            os.makedirs(directory)
        f.save(os.path.join(directory, filename))

        data = pd.read_csv(f'{directory}/{filename}', sep=';', header=None)
        data.columns = ['Raman shift', 'Intensity']
        fig = data.iplot(x='Raman shift', y='Intensity', asFigure=True,
                         title='Datos de ejemplo', xTitle='Longitud de onda',
                         yTitle='Valor'
                         )

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
    app.run_server(debug=True)
