import FuncionesEstado as F;
import pandas as pd
import Exclusiones as E


Entrada1 = [0,1,1,0,1,1,0,0,0,1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,0,0,0,1];
Entrada2 = [0,0,0,1,1,0,1,0,1,0,1,0,1,0,1,1,0,1,1,0,1,1,0,1,1,1,1,0,0,0];
Entrada3 = [0,1,0,1,0,1,0,1,0,1,1,0,1,1,0,1,1,1,1,0,1,0,1,0,1,0,1,0,1,0];


def CargarDatos():
    dataframe1 = pd.read_excel('Muestra7-8.xlsx', usecols="B:D",skiprows=[0,1],sheet_name="Muestra 8")

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

    Porcentajes = {
            '000':[100,0.0,0.0,0.0,0.0,0.0,0.0,0.0],
            '001':[0.0,100,0.0,0.0,0.0,0.0,0.0,0.0],
            '010':[0.0,0.0,0.0,0.0,0.0,100,0.0,0.0],
            '011':[0.0,0.0,0.0,0.0,0.0,100,0.0,0.0],
            '100':[0.0,0.0,0.0,0.0,100,0.0,0.0,0.0],
            '101':[0.0,0.0,0.0,0.0,0.0,0.0,0.0,100],
            '110':[0.0,100,0.0,0.0,0.0,0.0,0.0,0.0],
            '111':[0.0,0.0,0.0,100,0.0,0.0,0.0,0.0]
    }

    # for x in Porcentajes.keys():
    #     print(x+str(Porcentajes[x]))

    # print("-----------------------------------------------------------")
    # Resultados = F.DivisionElementos("ABC/AC=10",Porcentajes)
    # print(Resultados)

    # Primero = F.DivisionElementos("AB/AC=10",Porcentajes)
    # print(Primero)
    # Segundo = F.DivisionElementos("C/0",Porcentajes)
    # print(Segundo)
    # Mul ={}
    # Mul['A']= Primero
    # Mul['B']= Segundo

    # print(E.Multiplicar(Mul))
    # distancia = E.EMD(Resultados,E.Multiplicar(Mul))
    # print(distancia)

    # print("-----------------------------------------------------------")
    # Resultados = F.DivisionElementos("ABC/ABC=100",Porcentajes)
    # print(Resultados)

    # print("-----------------------")
    # Primero = F.DivisionElementos("AC/ABC=100",Porcentajes)
    # print(Primero)
    # Segundo = F.DivisionElementos("B/0",Porcentajes)
    # print(Segundo)
    # Mul ={}
    # Mul['A']= Primero
    # Mul['B']= Segundo

    # distancia = E.EMD(Resultados,E.Multiplicar(Mul))
    # print(distancia)

    # print("-----------------------------------------------------------")
    # Resultados = F.DivisionElementos("ABC/AC=10",Porcentajes)
    # print(Resultados)

    # Primero = F.DivisionElementos("0/A",Porcentajes)
    # print(Primero)
    # Segundo = F.DivisionElementos("ABC/C=10",Porcentajes)
    # print(Segundo)
    # Mul ={}
    # Mul['A']= Primero
    # Mul['B']= Segundo

    # print(E.Multiplicar(Mul))
    # distancia = E.EMD(Resultados,E.Multiplicar(Mul))
    # print(distancia)
    
    # Segundo = F.DivisionElementos("C/0",Porcentajes)
    Segundo = F.DivisionElementos("0/A",Porcentajes)
    print(Segundo)



CrearEstados(CargarDatos()[0]);
# CrearEstados([Entrada1,Entrada2,Entrada3]);



    # -----------------------------------------------------------------------------------------
    # Convertir el diccionario en una lista de arreglos de NumPy
    # data_array_list = list(Porcentajes.values())

    # # Convertir la lista en un arreglo de NumPy
    # tpm = np.array(data_array_list)

    # cm = np.array([
    #     [0, 1, 1],
    #     [1, 0, 1],
    #     [1, 1, 0],
    # ])

    # network = pyphi.Network(tpm, cm=cm, node_labels=['A', 'B', 'C'])
    # state = (1,0,0)
    # nodes = ('A', 'B', 'C')
    # subsystem = pyphi.Subsystem(network, state, nodes)

    # A, B, C = subsystem.node_indices

    # mechanism = (A, B, C)
    # purview = (A, C)
    # mip = subsystem.effect_mip(mechanism, purview)
    # print(mip)

    # mip_c = subsystem.cause_mip(mechanism, purview)
    # print(mip_c)

    # ces = pyphi.compute.ces(subsystem)
    # print(ces.labeled_mechanisms)





#----------------------------------------------------------------------------------------------------------------------
# A = F.DivisionElementos("ABC/A=0",Porcentajes)
    # # ------------- GRAFICA
    # B = ['000', '001', '010', '011', '100', '101', '110', '111']

    # # Crear un DataFrame de Pandas
    # df = pd.DataFrame({'Probabilidades': A, 'Estados': B})

    # # Colores para las barras
    # colores = ['blue', 'green', 'red', 'purple', 'orange', 'brown', 'pink', 'gray']

    # # Graficar con Matplotlib
    # fig, ax = plt.subplots()
    # barras = ax.bar(df['Estados'], df['Probabilidades'], color=colores)

    # # Mostrar las probabilidades dentro de las barras
    # for bar, prob in zip(barras, A):
    #     height = bar.get_height()
    #     ax.text(bar.get_x() + bar.get_width() / 2, height, f'{prob:.2f}', ha='center', va='bottom')

    # plt.xlabel('Estados')
    # plt.ylabel('Probabilidades')
    # plt.title('Grafica de las probabilidades')
    # plt.show()

