import src.funcionesEstado as F
import pandas as pd
import src.exclusiones as E
import tests.funciones_tests as T
import sys
import json

Entrada1 = [0,1,1,0,1,1,0,0,0,1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,0,0,0,1];
Entrada2 = [0,0,0,1,1,0,1,0,1,0,1,0,1,0,1,1,0,1,1,0,1,1,0,1,1,1,1,0,0,0];
Entrada3 = [0,1,0,1,0,1,0,1,0,1,1,0,1,1,0,1,1,1,1,0,1,0,1,0,1,0,1,0,1,0];

def CargarDatos():
    dataframe1 = pd.read_excel('data/Muestra7-8.xlsx', usecols="B:D",skiprows=[0,1],sheet_name="Muestra 8")

    dataframe1 = dataframe1.values.tolist()
    nuevos_arrays = [[] for _ in range(len(dataframe1[0]))]

    for x in range(len(dataframe1)):
        for y in range(len(dataframe1[0])):
            nuevos_arrays[y].append(dataframe1[x][y])

    return[nuevos_arrays]

def EncontrarPosiciones(Estados,Array):
    Posiciones=[]
    for i in range(len(Estados)):
        Posiciones.append([Estados[i]]);
    for m in range(len(Estados)):
        Valor = Estados[m];
        for x in range(len(Array[0])):
            if ''.join(str(Array[i][x]) for i in range(len(Array))) == str(Valor):
                Posiciones[m].append(x + 1)
    return Posiciones;

# Encontrar posiciones pasadas al canal dado
def EncontrarPosicionesR(Posiciones):
    arregloR = []
    for sublista in Posiciones:
        nueva_sublista = [sublista[0]]

        for valor in sublista[1:]:
            if valor > 1:
                nuevo_valor = valor - 2
                nueva_sublista.append(nuevo_valor)

        arregloR.append(nueva_sublista)

    return arregloR

def CrearEstados(Array):
    Porcentajes ={};
    Estados =[];
    Estadoinicial="";
    Estadoinicial = Estadoinicial.zfill(len(Array));
    Estados.append(Estadoinicial)
    siquiente = Estadoinicial;
    for i in range((2**len(Array))-1):
        siquiente = '{:b}'.format(int(siquiente,2)+int(1))
        Estados.append(siquiente.zfill(len(Array)))
    Posiciones= EncontrarPosiciones(Estados,Array);
    PosicionesR= EncontrarPosicionesR(Posiciones);

    Porcentajes = F.EstadoEstadoF(Array,Posiciones,Estados)

    # ---------------------------------------------
    # Matriz de Pruebas
    Porcentajes = T.matriz()
    # ---------------------------------------------

    # for x in Porcentajes.keys():
    #     print(x+str(Porcentajes[x]))


    ## Casos de pruebas -----------------------------
    # futuros_list = ['0', 'A','B','C']
    # presentes_list = ['0', 'A','C']
    # estado = "10"

    # # futuros_list = ['0', 'A','C']
    # # presentes_list = ['0', 'A','B','C']
    # # estado = "100"


    # # futuros_list = ['0','A','B']
    # # presentes_list = ['0','C']
    # # estado = "0"
    ## ---------------------------------------------


    # Verificar si se proporcionan suficientes argumentos
    if len(sys.argv) != 4:
        print("Data: <futuros> <presentes> <estado>")
        sys.exit(1)

    # Obtener las variables de la línea de comandos
    futuros = sys.argv[1]
    presentes = sys.argv[2]
    estado = sys.argv[3]

    futuros_list = ['0'] + list(futuros)
    presentes_list = ['0'] + list(presentes)
   
    # T.funciones_pruebas(Porcentajes) # Funciones de pruebas
    # F.posibles_soluciones(futuros_list, presentes_list, estado, Porcentajes) # funcion para realizar pruebas
    dic_data = F.solucion_minima(futuros_list, presentes_list, estado, Porcentajes) # funcion factible

    return dic_data

def main():
    # CrearEstados([Entrada1,Entrada2,Entrada3]);
    salida = CrearEstados(CargarDatos()[0])
    json_salida = json.dumps(salida)
    print(json_salida)  # Imprime la cadena JSON
    return json_salida


if __name__ == "__main__":
    main()
