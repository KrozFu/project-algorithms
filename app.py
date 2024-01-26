import dash
from dash import dcc, html  # Importa dcc y html directamente desde dash
from dash.dependencies import Input, Output, State
import re
import subprocess
import json

app = dash.Dash(__name__)

# Colores para diferenciar en las gráficas
colores_conjunto_2_3 = ['#ff7f0e',' #4dbd4b']

app.layout = html.Div(children=[
    html.Div([
        html.H1('Proyecto de Análisis y Diseño de Algoritmos'),
        html.Img(src='assets/img/logo.png')
    ], className = 'banner'),

    html.Div([
        html.Label('Futuros', style={'display': 'block'}),
        dcc.Input(id='futuros', type='text', placeholder='futuros', pattern='^[A-Za-z]+$'),

        html.Label('Presentes', style={'display': 'block'}),
        dcc.Input(id='presentes', type='text', placeholder='presentes', pattern='^[A-Za-z]+$'),

        html.Label('Estado', style={'display': 'block'}),
        dcc.Input(id='estado', type='number', placeholder='estado', min=0, step=1),

        html.Button('Enviar a consola', id='enviar-button', n_clicks=0)
    ], style={'textAlign': 'center', 'margin-top': '20px'}),

    html.Div(id='output-container', style={'marginTop': 20}),

    # Gráficos para los conjuntos
    dcc.Graph(id='grafica-conjunto-1'),
    dcc.Graph(id='grafica-conjunto-2'),
    dcc.Graph(id='grafica-conjunto-3'),
])

# Definir una función de devolución de llamada para actualizar el contenedor de salida
@app.callback(
    [Output('output-container', 'children'),
     Output('grafica-conjunto-1', 'figure'),
     Output('grafica-conjunto-2', 'figure'),
     Output('grafica-conjunto-3', 'figure')],
    [Input('enviar-button', 'n_clicks')],
    [State('futuros', 'value'),
     State('presentes', 'value'),
     State('estado', 'value')]
)
def update_output(n_clicks, futuros, presentes, estado):
    try:
        # Verificar si el botón ha sido clickeado
        if n_clicks > 0:
            # Validar que solo se hayan ingresado letras, y valida si son mayusculas
            if re.match('^[A-Za-z]+$', futuros) and re.match('^[A-Za-z]+$', presentes) and isinstance(estado, int) and estado >= 0:

                futuros = futuros.upper()
                presentes = presentes.upper()

                # subprocess.run(["python", "main.py", futuros, presentes, str(estado)])
                try:
                    output = subprocess.check_output(["python", "main.py", futuros, presentes, str(estado)], text=True)
                except subprocess.CalledProcessError as e:
                    print(f"Error al ejecutar main.py: {e}")
                    raise e

                datos = json.loads(output)
                # print(f"Salida del script: {output}")

                # Gráficos para los conjuntos
                fig_conjunto_1 = {
                    'data': [
                        {'x': [f'Valor {i + 1}' for i in range(len(datos["conjunto_1"][1]["valores"]))],
                         'y': datos["conjunto_1"][1]["valores"],
                         'type': 'bar',
                         'name': f'conjunto_1 - {datos["conjunto_1"][0]["caso"]}'}
                    ],
                    'layout': {
                        'title': f'Gráfica {datos["conjunto_1"][0]["caso"]}',
                        'barmode': 'group'
                    }
                }

                fig_conjunto_2 = {
                    'data': [
                        {'x': [f'Valor {i + 1}' for i in range(len(datos["conjunto_2"][1]["valores"]))],
                        'y': datos["conjunto_2"][1]["valores"],
                        'type': 'bar',
                        'name': f'conjunto_2 - {datos["conjunto_2"][0]["caso"]}',
                        'marker': {'color': colores_conjunto_2_3[0]}}  # Color específico para conjunto_2
                    ],
                    'layout': {
                        'title': f'Gráfica {datos["conjunto_2"][0]["caso"]}',
                        'barmode': 'group'
                    }
                }

                fig_conjunto_3 = {
                    'data': [
                        {'x': [f'Valor {i + 1}' for i in range(len(datos["conjunto_3"][1]["valores"]))],
                        'y': datos["conjunto_3"][1]["valores"],
                        'type': 'bar',
                        'name': f'conjunto_3 - {datos["conjunto_3"][0]["caso"]}',
                        'marker': {'color': colores_conjunto_2_3[1]}}  # Mismo color que conjunto_2
                    ],
                    'layout': {
                        'title': f'Gráfica {datos["conjunto_3"][0]["caso"]}',
                        'barmode': 'group'
                    }
                }

                # Unir las gráficas de conjunto_2 y conjunto_3 en una sola figura
                combined_fig = {
                    'data': fig_conjunto_2['data'] + fig_conjunto_3['data'],
                    'layout': {
                        'title': f'Gráficas de {datos["conjunto_2"][0]["caso"]} y {datos["conjunto_3"][0]["caso"]}',
                        'barmode': 'group'
                    }
                }

                return f'Datos Cargados {n_clicks}.', fig_conjunto_1, combined_fig, None
            else:
                return 'Error: Ingresa solo letras del alfabeto para futuros y presentes, y valores numéricos enteros positivos para estado.', None

    except Exception as e:
        print(f"Error en la función de devolución de llamada: {e}")
        raise e

    return '', None  # No se muestra nada si no se ha clickeado

if __name__ == '__main__':
    app.run_server()
    # app.run_server(debug=True)
