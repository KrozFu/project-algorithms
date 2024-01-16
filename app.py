import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import re
import subprocess

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.Div(
        html.H1('Proyecto', style={'color': '#ffffff'}),
        className='banner'
    ),

    html.H1(
        children='Proyecto de Análisis y Diseño de Algoritmos',
        style={'textAlign': 'center'}
    ),
    html.Div(
        children='Framework para aplicaciones web con Python',
        style={'textAlign': 'center', 'margin-bottom': '20px'}
    ),

    html.Div([
        html.Label('Futuros'),
        dcc.Input(id='futuros', type='text', placeholder='futuros', pattern='^[A-Za-z]+$'),

        html.Label('Presentes'),
        dcc.Input(id='presentes', type='text', placeholder='presentes', pattern='^[A-Za-z]+$'),

        html.Label('Estado'),
        dcc.Input(id='estado', type='number', placeholder='estado', min=0, step=1),

        html.Button('Enviar a consola', id='enviar-button', n_clicks=0)
    ], style={'textAlign': 'center', 'margin-top': '20px'}),

    html.Div(id='output-container', style={'marginTop': 20}),
])

# Definir una función de devolución de llamada para actualizar el contenedor de salida
@app.callback(
    Output('output-container', 'children'),
    [Input('enviar-button', 'n_clicks')],
    [State('futuros', 'value'),
     State('presentes', 'value'),
     State('estado', 'value')]
)
def update_output(n_clicks, futuros, presentes, estado):
    # Verificar si el botón ha sido clickeado
    if n_clicks > 0:
        # Validar que solo se hayan ingresado letras, y valida si son mayusculas
        if re.match('^[A-Za-z]+$', futuros) and re.match('^[A-Za-z]+$', presentes) and isinstance(estado, int) and estado >= 0:

            futuros = futuros.upper()
            presentes = presentes.upper()
            
            subprocess.run(["python", "main.py", futuros, presentes, str(estado)])

            return f'Datos Cargados {n_clicks}'
        else:
            return 'Error: Ingresa solo letras del alfabeto para futuros y presentes, y valores numéricos enteros positivos para estado.'

    return ''  # No se muestra nada si no se ha clickeado

if __name__ == '__main__':
    app.run_server()
