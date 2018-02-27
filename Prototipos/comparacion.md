# Jupyter notebook + Plotly
## Pros
* Fácil subir archivos
* Permite centrarse en programar el código de minería de datos
* Plotly dentro del notebook
* Uso de [Binder](https://mybinder.org/) para el despliegue, se asocia al repositorio (soluciona problema de solo un usuario)
* Actualización por medio de `interact` u `observe`
* Posibilidad de convertir gráficos de matplotlib a Plotly
* Unir pandas y Plotly con cufflinks
## Contras
* Menos bonito y usable
* Código expuesto
* [Solo se puede un usuario](http://jupyter-notebook.readthedocs.io/en/latest/public_server.html)
* Dos formas de representar, online u offline


# Flask + Dash
## Pros
* Gráficos interactivos
* Fácil actualización en vivo del gráfico mediante `@app.callback`
* Más bonito y usable
* Subida de ficheros manejada por Flask
* Posibilidad de convertir gráficos de matplotlib a Plotly
* Unir pandas y Plotly con cufflinks
## Contras
* Difícil escritura de HTML al tener que escribirse programaticamente
* Gráfico en un pestaña aparte, posiblemente sin el mismo formato del resto de la web por la desventaja anterior


# Flask + Plotly
## Pros
* Gráficos interactivos
* Facíl de incrustar el gráfico en HTML
* Subida de ficheros manejada por Flask
* Posibilidad de convertir gráficos de matplotlib a Plotly
* Unir pandas y Plotly con cufflinks
## Contras
* Más dificultad a la hora de actualizar el gráfico en vivo
* Uso de dos librerías en lenguajes diferentes, Plotly.py y Plotly.js
* Dos formas de representar, online u offline
