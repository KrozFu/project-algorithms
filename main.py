import src.funcionesEstado as F
import pandas as pd
import src.exclusiones as E
import tests.funciones_tests as T

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

    # Matriz de Pruebas
    Porcentajes = T.matriz()

    # for x in Porcentajes.keys():
    #     print(x+str(Porcentajes[x]))

    # T.funciones_pruebas(Porcentajes)

    vector1 = ['0', 'A', 'B', 'C']
    vector2 = ['0', 'A', 'C']
    estado = "10"

    generar_posibles_casos(vector1, vector2,estado,Porcentajes)


def generar_posibles_casos(vector1, vector2, estado, porcentajes):
    string1 = ''.join(x for x in vector1[1:])
    string2 = ''.join(x for x in vector2[1:])
    
    caso_base = str(string1+"/"+string2+"="+estado)
    
    dic_val_presentes = {}
    # Verificar que las longitudes de ambas cadenas sean iguales
    if len(string2) != len(estado):
        print("Las longitudes de las cadenas no son iguales.")
    else:
        for i in range(len(string2)):
            dic_val_presentes[string2[i]] = estado[i]

    resultados = F.DivisionElementos(caso_base,porcentajes)
    print("Caso Base")
    print(resultados)
    print("-----------------------------------------------------------")

    combinaciones = F.generar_combinaciones(vector1,vector2)
    # print(combinaciones)

    for llave, valores in combinaciones.items():
        caso1 = valores[0]
        caso2 = valores[1]

        res1 = caso1.split("/")[1]
        res2 = caso2.split("/")[1]

        resultado_val = ""

        if res1 != "0":
            for caracter in res1:
                if caracter in dic_val_presentes:
                    resultado_val += dic_val_presentes[caracter]
            caso1 = caso1+"="+resultado_val
        else:
            caso1 = caso1

        resultado_val = ""
        if res2 != "0":
            for caracter in res2:
                if caracter in dic_val_presentes:
                    resultado_val += dic_val_presentes[caracter]
            caso2 = caso2+"="+resultado_val
        else:
            caso2 = caso2

        # # Imprime los valores para comprobar
        print(f"caso1: {caso1}, -- ,caso2: {caso2}")

            
        Primero = F.DivisionElementos(caso1,porcentajes)
        print(Primero)
        Segundo = F.DivisionElementos(caso2,porcentajes)
        print(Segundo)
        Mul ={}
        Mul['A']= Primero
        Mul['B']= Segundo

        distancia = E.EMD(resultados, E.Multiplicar(Mul))
        print(f"EMD={distancia}")
        print("-----------------------------------------------------------")


def main():
    CrearEstados(CargarDatos()[0]);
    # CrearEstados([Entrada1,Entrada2,Entrada3]);

if __name__ == "__main__":
    main()
