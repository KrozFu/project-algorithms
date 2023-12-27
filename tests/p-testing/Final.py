import streamlit as st
import pandas as pd
import string
import matplotlib.pyplot as plt
import numpy as np
from itertools import product
from itertools import combinations
import copy
import time

# pip install pandas
# pip install matplotlib
# pip install numpy
# pip install pillow
# pip install streamlit

matriz = []
vector = []
valores_letras = {
    'A': 0,
    'B': 1,
    'C': 2,
    'D': 3,
    'E': 4,
    'F': 5,
    'G': 6,
    'H': 7,
    'I': 8,
    'J': 9,
    'K': 10,
    'L': 11,
    'M': 12,
    'N': 13,
    'O': 14,
    'P': 15,
    'Q': 16,
    'R': 17,
    'S': 18,
    'T': 19,
    'U': 20,
    'V': 21,
    'W': 22,
    'X': 23,
    'Y': 24,
    'Z': 25
}

def leer_matriz_desde_texto(contenido):
    matriz = []

    try:
        lineas = contenido.splitlines()

        for linea in lineas:
            valores = linea.strip().split(",")
            fila_binaria = []

            for valor in valores:
                try:
                    valor_binario = int(valor)
                    if valor_binario != 0 and valor_binario != 1:
                        raise ValueError("Los valores deben ser 0 o 1.")
                    fila_binaria.append(valor_binario)
                except ValueError:
                    st.error("Error: Los valores deben ser 0 o 1.")
                    return None

            matriz.append(fila_binaria)

        return matriz

    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

def generar_casos(matriz):
    num_filas = len(matriz) # Obtener el número de filas en la matriz
    casos = []

    def generar_combinaciones(fila_actual, indice): # Se Define una función interna para generar combinaciones recursivamente
        if indice == num_filas:
            casos.append(list(fila_actual))
            return
        fila_actual[indice] = 0
        generar_combinaciones(fila_actual, indice + 1) # Se llama recursivamente para el siguiente indice
        fila_actual[indice] = 1
        generar_combinaciones(fila_actual, indice + 1)

    fila_actual = [0] * num_filas
    generar_combinaciones(fila_actual, 0) # Genera las combinations desde el indice 0

    return casos

def convertir_letras_a_valores_entrega3(letras):
    valores = []
    letras = letras.upper().split()  # Convertir todo a mayúsculas y dividir por espacios
    for letra in letras:
        if letra in valores_letras:
            valores.append(str(valores_letras[letra]))  # Convertir el valor a cadena antes de agregarlo
        else:
            valores.append(None)  # o manejar valores no válidos según sea necesario
    return ' '.join(valores)  # Unir los valores en una cadena separados por espacio

def convertir_letras_a_valores_entrega4(letras):
    valores = []
    letras = letras.upper().split()  # Convertir todo a mayúsculas y dividir por espacios
    for letra in letras:
        if letra in valores_letras:
            valores.append(valores_letras[letra]+1)  # Convertir el valor a cadena antes de agregarlo
        else:
            valores.append(None)  # o manejar valores no válidos según sea necesario
    return valores  # Unir los valores en una cadena separados por espacio

# Función para calcular el producto de Kronecker de una lista de matrices
def MatricesKronecker(matrix_list):
    result = matrix_list[0]
    for matrix in matrix_list[1:]:
        result = ProductoKronecker(result, matrix)
    return result

# Función para calcular el producto de Kronecker de dos matrices
def ProductoKronecker(A, B):
    m, n = A.shape
    p, q = B.shape

    result = [[0] * (n * q) for _ in range(m * p)]

    for i in range(m):
        for j in range(n):
            for k in range(p):
                for l in range(q):
                    result[i * p + k][j * q + l] = A[i, j] * B[k, l]

    return np.array(result)

# Función para calcular la distancia EMD entre dos histogramas
def earth_movers_distance(hist1, hist2):
    # Rellena el histograma más corto con ceros hasta que tenga la misma longitud que el histograma más largo
    if len(hist1) < len(hist2):
        hist1 = np.pad(hist1, (0, len(hist2) - len(hist1)), 'constant')
    elif len(hist2) < len(hist1):
        hist2 = np.pad(hist2, (0, len(hist1) - len(hist2)), 'constant')

    n = len(hist1)
    total_distance = 0.0
    cumulative_diff = 0.0

    for i in range(n):
        diff = hist1[i] - hist2[i]
        cumulative_diff += diff
        total_distance += abs(cumulative_diff)

    # Redondear el resultado a 2 decimales
    return round(total_distance, 2)

#Funcion que genera las posibles combinaciones para descomponer el sistema
def CombinEstados(futuro,actual):
        IndicesSelec=[]
        segListaCombi = [list(comb) for longitud in range(1, len(actual) + 1) for comb in combinations(actual, longitud)]
        priListaCombi = [list(comb) for longitud in range(1, len(futuro) + 1) for comb in combinations(futuro, longitud)]
        segListaCombi.insert(0,[0])
        priListaCombi.insert(0,[0])
        permutaciones = list(product(priListaCombi, segListaCombi))
        mid1 = permutaciones[:len(permutaciones)//2]
        mid2 = permutaciones[len(permutaciones)//2:]
        matrix=[]
        mid2.reverse()
        for i in range(0, len(mid1)):
            matrix.append([mid1[i], mid2[i]])
        listA =[]
        listB=[]
        listC=[]
        combMatrix = []
        for fila in matrix:
                for lista in fila:
                    for tupla in lista:
                        for index in tupla:
                                listA.append(index)
                        listC.append(listA)
                        listA=[]
                    listB.append(listC)
                    listC=[]
                combMatrix.append(listB)
                listB=[]
        IndicesSelec.append(futuro)
        IndicesSelec.append(actual)
        return combMatrix, IndicesSelec

#Convierte los casos
def converCasos(caso,IS):
        newMatrixo=[]
        indexs=[]
        if IS[0]==0:
            return IS
        if len(caso[0])==len(IS):
            return caso
        for i in caso:
            for j in IS:
                indexs.append(i[j-1])
            newMatrixo.append(indexs)
            indexs=[]
        return newMatrixo

#Convierte los estados
def converEstado2(matrizEstad,listaindexs):
    copiamatrizEstad = copy.deepcopy(matrizEstad)
    PrimerCaso, SegundoCaso, contenido = splitList(copiamatrizEstad)
    PrimerCaso = converCasos(PrimerCaso,listaindexs[0])
    SegundoCaso = converCasos(SegundoCaso,listaindexs[1])
    PrimerCasoFin, SegundoCasoFin, contenidoFinal= convertColumnas(PrimerCaso,contenido,SegundoCaso)
    return( PrimerCasoFin, SegundoCasoFin, contenidoFinal)

#Dividir la matriz
def splitList(mat):
    PrimerCaso = mat[0]
    SegundoCaso = mat[0]
    contenido= convertContent(mat[1:])
    return PrimerCaso, SegundoCaso, contenido

#Convertir las columnas
def convertColumnas(PrimerCaso,contenido, SegundoCaso):
    PrimerCasoCopy = []
    copiaContenido = []
    copiaFila = []
    cont = 0
    if PrimerCaso[0]==0:
        return sumarColumnas(PrimerCaso,contenido, SegundoCaso)
    else:
        for i in contenido:
                copiaContenido.append([])
        while(cont < len(PrimerCaso)):
            if(PrimerCaso[cont] in PrimerCasoCopy ):
                index = PrimerCasoCopy.index(PrimerCaso[cont])
                for i in range(len(contenido)):
                    fila= contenido[i]
                    copiaFila = copiaContenido[i]
                    copiaFila[index] = copiaFila[index]+fila[cont]
            else:
                PrimerCasoCopy.append(PrimerCaso[cont])
                for i in range (len(contenido)):
                    fila = contenido[i]
                    copiaFila = copiaContenido[i]
                    copiaFila.append(fila[cont])
            cont +=1
        return convertFilas(SegundoCaso, copiaContenido, PrimerCasoCopy)

def convertFilas(SegundoCaso,contenido, PrimerCasoF):
    casoCopy = []
    copiaContenido = []
    cont = 0
    div=1
    if SegundoCaso[0]==0:
        return sumarFilas(SegundoCaso,contenido, PrimerCasoF)
    else:
        
        while(cont < len(SegundoCaso)):
            if(SegundoCaso[cont] in casoCopy):
                if(SegundoCaso[cont] == SegundoCaso[0] ):
                    div += 1
                index = casoCopy.index(SegundoCaso[cont])
                fila=copiaContenido[index]
                segundaFila=contenido[cont]
                copiaContenido[index]= [(x + y) for x, y in zip(fila, segundaFila)]
                
            else:
                casoCopy.append(SegundoCaso[cont])
                copiaContenido.append(contenido[cont])
                
            cont +=1
        for i in  range(len(copiaContenido)):
            for j in range(len(copiaContenido[i])):
                copiaContenido[i][j]/=div
                copiaContenido[i][j]=round(copiaContenido[i][j],2)
        return PrimerCasoF,casoCopy, copiaContenido

def sumarFilas(SegundoCaso,contenido, PrimerCasoF):
    div=len(contenido)
    content_total = [sum(column) for column in zip(*contenido)]
    content_total = [round(elemento / div,2) for elemento in content_total]
    return (PrimerCasoF,SegundoCaso, content_total)

def sumarColumnas(PrimerCaso,contenido,SegundoCaso):
    sumFila = []
    for fila in contenido:
        suma_row = sum(fila)
        sumFila.insert(0,[suma_row]) 
    sumFila.reverse()
    return convertFilas(SegundoCaso,sumFila, PrimerCaso)

def convertContent(mat):
    MatNueva = []
    for lista in mat:
        temp = []
        del lista[0]
        for subList in lista:
            for  j in subList: 
                temp.append(j)
        MatNueva.append(temp)
        temp=[]
    return(MatNueva)

matriztransp=list(map(list, zip(*matriz))) #invierte la matriz para trabajarla mas sencillo, cambiando estados por canales y viceversa

def EstadoCanalFuturo(matriz,numEstSig,casos):
    #limpiar_pantalla()
    matriztransp=list(map(list, zip(*matriz)))
    totalCanales=[[0] * len(casos[0]) for asd in range(len(casos))] #Crea otra matriz para almacenar las coincidencias con el caso siguiente
    totalCoincidencias=[[0]*len(casos[0]) for asd in range(len(casos))] #Crea otra matriz para almacenar el numero de veces que esta la muestra en la matriz de casos base
    
    #Ciclo for para almacenar los valores en las respectivas matrices creadas anteriormente
    for c in range(len(casos)):
        for i in range(len(matriztransp)):
            if matriztransp[i] == casos[c] and i + numEstSig < len(matriztransp): #Verifica coincidencias entre el caso base seleccionado y la matriz principal
                for x in range(len(casos[c])):
                    totalCoincidencias[c][x]+=1
                    if(matriztransp[-1]==casos[c]): 
                        totalCoincidencias[c][x]+=1
                    if matriztransp[i + numEstSig][x] == 1: #Contador, si el valor que hay en el estado anterior cada n veces es = a 1
                        totalCanales[c][x] += 1
                        
    return totalCanales, totalCoincidencias

def EstadoCanalPasado(matriz,numEstAnt,casos):
    #limpiar_pantalla()
    matriztransp=list(map(list, zip(*matriz)))
    totalCanales=[[0] * len(casos[0]) for asd in range(len(casos))] #Crea otra matriz para almacenar las coincidencias con el caso anterior
    totalCoincidencias=[[0]*len(casos[0]) for asd in range(len(casos))] #Crea otra matriz para almacenar el numero de veces que esta la muestra en la matriz de casos base
    #print(casos)

    #Ciclo for para almacenar los valores en las respectivas matrices creadas anteriormente
    for c in range(len(casos)):
        for i in range(len(matriztransp)):
            if matriztransp[i] == casos[c] and i - numEstAnt >=0: #Verifica coincidencias entre el caso base seleccionado y la matriz principal
                for x in range(len(casos[c])):
                    totalCoincidencias[c][x]+=1
                    if(matriztransp[0]==casos[c]):
                        totalCoincidencias[c][x]+=1
                    if matriztransp[i - numEstAnt][x] == 1: #Contador, si el valor que hay en el estado anterior cada n veces es = a 1
                        totalCanales[c][x] += 1
    
    return totalCanales, totalCoincidencias

def EstadoEstadoF(matriz, intervalo):
    matriztransp = list(map(list, zip(*matriz))) # Transpone la matriz para que cada fila represente un Estado
    num_casos = len(matriztransp) # Obtiene el número de casos (columnas en la matriz)
    relacion_casos = {} # Crea un diccionario para almacenar las relaciones entre estados

    for i in range(num_casos - intervalo): # Itera a través de los casos hasta el índice que se encuentra a "intervalo" pasos del final
        caso_actual = tuple(matriztransp[i]) # Convierte la fila actual en una tupla
        caso_siguiente = tuple(matriztransp[i + intervalo]) # Convierte la fila "intervalo" pasos adelante en una tupla

        if caso_actual not in relacion_casos: # Verifica si el caso actual ya está en el diccionario de relaciones
            # Si no está, crea una entrada para él con un contador de ocurrencias igual a 1
            # y un diccionario vacío para almacenar las relaciones con casos siguientes
            relacion_casos[caso_actual] = {"ocurrencias": 1, "relaciones": {}}
        else:
            relacion_casos[caso_actual]["ocurrencias"] += 1 # Si ya existe, incrementa el contador de ocurrencias

        # Verifica si el caso siguiente ya está en el diccionario de relaciones del caso actual
        if caso_siguiente not in relacion_casos[caso_actual]["relaciones"]:
            relacion_casos[caso_actual]["relaciones"][caso_siguiente] = 1
        else:
        # Si ya existe, incrementa el contador de relaciones con el caso siguiente
            relacion_casos[caso_actual]["relaciones"][caso_siguiente] += 1
    return relacion_casos

def EstadoEstadoP(matriz, intervalo):
    # Transpone la matriz para que cada fila represente un canal en lugar de un estado
    matriztransp = list(map(list, zip(*matriz)))

    num_casos = len(matriztransp)  # Obtiene el número de casos (columnas en la matriz)
    relacion_casos = {}  # Crea un diccionario para almacenar las relaciones entre estados

    # Itera a través de los casos a partir del índice "intervalo" hasta el final
    for i in range(intervalo, num_casos):
        caso_actual = tuple(matriztransp[i])  # Convierte la fila actual en una tupla
        caso_anterior = tuple(matriztransp[i - intervalo])  # Convierte la fila "intervalo" pasos atrás en una tupla

        # Verifica si el caso actual ya está en el diccionario de relaciones
        if caso_actual not in relacion_casos:
            # Si no está, crea una entrada para él con un contador de ocurrencias igual a 1
            # y un diccionario vacío para almacenar las relaciones con casos anteriores
            relacion_casos[caso_actual] = {"ocurrencias": 1, "relaciones": {}}
        else:
            # Si ya existe, incrementa el contador de ocurrencias
            relacion_casos[caso_actual]["ocurrencias"] += 1

        # Verifica si el caso anterior ya está en el diccionario de relaciones del caso actual
        if caso_anterior not in relacion_casos[caso_actual]["relaciones"]:
            # Si no está, crea una entrada para él con un contador igual a 1
            relacion_casos[caso_actual]["relaciones"][caso_anterior] = 1
        else:
            # Si ya existe, incrementa el contador de relaciones con el caso anterior
            relacion_casos[caso_actual]["relaciones"][caso_anterior] += 1

    return relacion_casos  # Devuelve el diccionario de relaciones entre estados anteriores
#---------------------------------------------------Interfaz---------------------------------------------------#
def mostrar_resultados(totalCanales, totalCoincidencias, casos):
    letras = list(string.ascii_uppercase)
    data = []
    for i in range(len(totalCanales)):
        fila = []
        for j in range(len(totalCanales[i])):
            # Verificar si totalCoincidencias[i][j] es cero
            if totalCoincidencias[i][j] == 0:
                resultado = 0  # O puedes usar None o np.nan si prefieres representar un valor indefinido
            else:
                resultado = round(totalCanales[i][j]/totalCoincidencias[i][j], 3)
            fila.append(resultado)
        data.append([str(casos[i])] + fila)


    column_names = ["Estados"] + letras[:len(totalCanales[0])]
    df = pd.DataFrame(data, columns=column_names)
    st.dataframe(df)

def imprimir_tabla_relaciones_binarias(casos, relacion_casos):
    vector_tabla = []
    vector_tabla.append(casos)  # Agregando los casos como una lista de listas
    estados = casos  # Los casos ya son listas de listas

    data = []

    for i, caso_actual in enumerate(estados):
        relacion_caso = [caso_actual]  # Agregar estado actual como lista
        for j, caso_siguiente in enumerate(estados):
            caso_siguiente_tuple = tuple(caso_siguiente)
            if caso_siguiente_tuple in relacion_casos.get(tuple(caso_actual), {}).get("relaciones", {}):
                ocurrencias = relacion_casos[tuple(caso_actual)]["relaciones"][caso_siguiente_tuple]
                total_ocurrencias = relacion_casos[tuple(caso_actual)]['ocurrencias']
                valor_decimal = ocurrencias / total_ocurrencias if total_ocurrencias != 0 else 0.0
                relacion_caso.append([round(valor_decimal, 1)])  # Envolver el valor en una lista
            else:
                relacion_caso.append([0.0])  # Envolver el valor por defecto en una lista
        data.append(relacion_caso)
        vector_tabla.append(relacion_caso)  # Almacenar la fila en el vector

    # Mostrar la tabla en Streamlit
    st.table(data)
    vector = vector_tabla
    st.session_state.vector = vector

    return st.session_state.vector

def mostrar_datos_opc4(indice_columnas,indice_filas, contenido_tabla):
    column_names = [f"{i:03b}" for i in range(len(indice_columnas))]
    data = []

    for i in range(len(indice_filas)):
        fila = "".join(map(str, indice_filas[i]))
        valores = [contenido_tabla[i][valor] for valor in range(len(contenido_tabla[i]))]
        data.append([fila] + valores)

    df = pd.DataFrame(data, columns=[""] + column_names)
    st.dataframe(df)

def graficarTablas(categorias, valores):
    categorias_str = [str(cat) for cat in categorias]
    fig, ax = plt.subplots()
    fig.patch.set_facecolor('gray')  # Cambia el color de fondo
    ancho_barras = 0.35
    posiciones_categorias = np.arange(len(categorias_str))

    colores = ['skyblue', 'lightgreen']  # Colores personalizados

    for i, valor_categoria in enumerate(valores):
        barras = ax.bar(posiciones_categorias + i * ancho_barras, valor_categoria, width=ancho_barras, label=f"Grafica {'Original' if i == 0 else 'EMD'}", color=colores[i])
        # Añadir etiquetas a las barras solo si la altura es mayor que 0
        for barra in barras:
            altura = barra.get_height()
            if altura > 0:
                ax.annotate(f'{altura:.2f}',
                            xy=(barra.get_x() + barra.get_width() / 2, altura),
                            xytext=(0, 3),  # 3 puntos de desplazamiento vertical
                            textcoords="offset points",
                            ha='center', va='bottom')

    ax.set_xlabel('Estados')
    ax.set_ylabel('Valores')
    ax.set_title('Comparación de Estados')
    ax.set_xticks(posiciones_categorias + ancho_barras / 2)
    ax.set_xticklabels(categorias_str)
    ax.legend()
    ax.grid(True)  # Añadir cuadrícula

    st.pyplot(fig)

def limpiar():
    df = pd.DataFrame()

# Función para convertir números a letras
def convertir_a_letras(combinacion_numeros):
    # Tu código aquí
    pass

# Función para actualizar la etiqueta de la consola
def actualizar_etiqueta(emd, combinacion):
    st.write(f"Menor distancia EMD: {emd}")


#---------------------------------------------------Funciones de las tablas---------------------------------------------------#
def MostrarMatriz(matriz):
    if not matriz:
        st.error("No has creado una lista para imprimir")
    else:
        nombres_columnas = [f"T{i+1}" for i in range(len(matriz[0]))]
        nombres_filas = [f"Canal {chr(65 + i)}" for i in range(len(matriz))]

        # Convertir la matriz a un DataFrame de Pandas
        df = pd.DataFrame(matriz, columns=nombres_columnas, index=nombres_filas)

        # Mostrar el DataFrame como una tabla en Streamlit
        st.dataframe(df)

def EstadoEstado(matriz):
    inicioEstado = time.time()
    casos = generar_casos(matriz)
    

    imprimir_tabla_relaciones_binarias(casos, EstadoEstadoF(matriz, 1))
    finEstado = time.time()
    tiempo_transcurrido_estado = finEstado - inicioEstado
    st.write(f"Tiempo de ejecución de estado: {tiempo_transcurrido_estado} segundos")

def EstadoCanal(matriz): 
    inicioCanal = time.time()
    casos = generar_casos(matriz)
    
    totalCanales, totalCoincidencias = EstadoCanalFuturo(matriz, 1, casos)
    mostrar_resultados(totalCanales, totalCoincidencias, casos)
    finCanal = time.time()
    tiempo_transcurrido_canal = finCanal - inicioCanal
    st.write(f"Tiempo de ejecución de canal: {tiempo_transcurrido_canal} segundos")

def Marginalizacion(vector):
    if not matriz:
        st.error("No has creado una lista para operar")
    elif not vector:
        st.error("No has generado la matriz EstadoEstado futuro")
    else:

        letras_columnas = st.text_input("Estado Actual a evaluar, separados por espacios (A B C)")
        letras_filas = st.text_input("Estados Futuros a evaluar, separados por espacios (A B C)")
        inicio1 = time.time()
        valores_filas = convertir_letras_a_valores_entrega3(letras_filas)
        valores_columnas = convertir_letras_a_valores_entrega3(letras_columnas)
        fin1 = time.time()
        tiempo_transcurrido_1 = fin1 - inicio1

        def convertirCasos(c,caso):
            nuevamatriz=[]
            indices=[]
            indices_seleccionados = c
            indices_seleccionados= list(map(int, c.split()))
            for i in caso:
                for j in indices_seleccionados:
                    indices.append(i[j-1])
                nuevamatriz.append(indices)
                indices=[]
            return nuevamatriz

        def convertircolumnas(caso1,contenido):
            caso1Copia = []
            contenidoCopia = []
            contador = 0
            for i in contenido:
                    contenidoCopia.append([])
            # aqui creamos filas para nuestra matriz copia
            while(contador < len(caso1)):
                if(caso1[contador] in caso1Copia):
                    indice = caso1Copia.index(caso1[contador])# encontrar el index caso1Copia
                    #con el indice vamos a el contenido copia y le sumamos los elementos de la misma columna del contenido original
                    for i in range(len(contenido)):
                        fila= contenido[i] # fila del contenido original 
                        filacopia = contenidoCopia[i] #fila de la copia

                        filacopia[indice] = filacopia[indice]+fila[contador]
                else:
                    caso1Copia.append(caso1[contador])
                    for j in range (len(contenido)):
                        fila = contenido[j]
                        filacopia = contenidoCopia[j]
                        filacopia.append(fila[contador])
                contador +=1
            return caso1Copia, contenidoCopia

        def convertirfilas(caso2,contenido):
            casoCopia = []
            contenidoCopia = []
            contador = 0
            divisor=1
            while(contador < len(caso2)):
                if(caso2[contador] in casoCopia):
                    if(caso2[contador] == caso2[0] ):
                        divisor += 1
                    indice = casoCopia.index(caso2[contador])
                    #con el indice vamos a el contenido copia y le sumamos los elementos de la misma fila del contenido original
                    fila=contenidoCopia[indice]
                    fila2=contenido[contador]
                    contenidoCopia[indice]= [(x + y) for x, y in zip(fila, fila2)]
                    
                    # directame los elementos de la columna
                else:
                    casoCopia.append(caso2[contador])
                    contenidoCopia.append(contenido[contador])
                    
                contador +=1
            for i in  range(len(contenidoCopia)):
                for j in range(len(contenidoCopia[i])):
                    contenidoCopia[i][j]/=divisor
            return casoCopia, contenidoCopia

        def convertircontenido(matriz):
            nueva_matriz = []
            matrizTemp= matriz
            for lista in matrizTemp:
                nueva_lista = []
                for sublista in lista[1:]:
                    for  j in sublista: 
                        nueva_lista.append(j)
                nueva_matriz.append(nueva_lista)
                nueva_lista=[]
            return(nueva_matriz)
        
        def partir_lista(matriz):
            caso1 = matriz[0]
            caso2 = matriz[0]
            contenido= convertircontenido(matriz[1:])
            return caso1, caso2, contenido
        
        inicio2 = time.time()
        t1, t2, c = partir_lista(vector)
        t1 = convertirCasos(valores_filas,t1)
        t2 = convertirCasos(valores_columnas,t2)
        t1n, cn= convertircolumnas(t1,c)
        t2n, cf = convertirfilas(t2,cn)
        fin2 = time.time()
        tiempo_transcurrido_2 = fin2 - inicio2

        # Mostrar los resultados como una tabla
        indice_columnas_str = [''.join(map(str, col)) for col in t1n]
        indice_filas_str = [''.join(map(str, fila)) for fila in t2n]

        datos = {indice_columnas_str[i]: [cf[j][i] for j in range(len(cf))] for i in range(len(indice_columnas_str))}
        df = pd.DataFrame(datos, index=indice_filas_str, columns=indice_columnas_str)
        st.dataframe(df)

        if 'comp_input' not in st.session_state:
            st.session_state.comp_input = ""
        if 'procesar_estado' not in st.session_state:
            st.session_state.procesar_estado = False

        if len(indice_filas_str) == 2:
            comp_input = st.text_input('Con qué fila desea compararlo? 0 o 1', st.session_state.comp_input)
        elif len(indice_filas_str) == 4:
            comp_input = st.text_input('Con qué fila desea compararlo? Formato: 0 0', st.session_state.comp_input)
        else:
            comp_input = st.text_input('Con qué fila desea compararlo? Formato: 0 0 0', st.session_state.comp_input)

        st.session_state.comp_input = comp_input

        if st.button("Procesar", key="btn_procesar"):
            st.session_state.procesar_estado = True
        inicio3 = time.time()          
        if st.session_state.procesar_estado:
            if comp_input:
                comp = [int(valor) for valor in comp_input.split()]
                if comp in t2n:
                    index = t2n.index(comp)
                    graficarTablas(t1n, [cf[index]])
                else:
                    st.error("La fila digitada no se encuentra en las generadas por el programa")
        fin3 = time.time()
        tiempo_transcurrido_3 = fin3 - inicio3
        tiempo_total = tiempo_transcurrido_3 + tiempo_transcurrido_2 + tiempo_transcurrido_1
        st.write(f"Tiempo de ejecución de marginalización: {tiempo_total} segundos")


def EMD(vector):

    P = []
    letras_columnas = st.text_input("Estado Actual a evaluar, separados por espacios (A B C)", key="letras_columnas")
    letras_filas = st.text_input("Estados Futuros a evaluar, separados por espacios (A B C)", key="letras_filas")


    global matriz


    if matriz == []:
        st.error("No has creado una lista para operar")
    elif vector == []:
        st.error("No has generado la matriz EstadoEstado futuro")
    else:

        inicio1 = time.time()
        valores_filas = convertir_letras_a_valores_entrega4(letras_filas)
        valores_columnas = convertir_letras_a_valores_entrega4(letras_columnas)

        combinacionesMatriz, matriz1 = CombinEstados(valores_filas, valores_columnas)
        MatrizOriginal = converEstado2(vector, matriz1)
        matrixoriginalstates = MatrizOriginal[1:2]
        matrixoriginalfirsttitle = MatrizOriginal[0:1]
        MatrizOriginal = np.array(MatrizOriginal[2:])
        fin1 = time.time()
        tiempo_transcurrido_1 = fin1 - inicio1
        try:
            if len(valores_columnas) == 2:
                comp = st.text_input('Con qué fila desea compararlo? Formato: 0 o 1', key="fila_comparacion").split()
            elif len(valores_columnas) == 4:
                comp = st.text_input('Con qué fila desea compararlo? Formato: (0 0)', key="fila_comparacion").split()
            else:
                comp = st.text_input('Con qué fila desea compararlo? Formato: (0 0 0)', key="fila_comparacion").split()
            
            comp = [int(valor) for valor in comp]

            # Verificar que la longitud de la entrada sea válida
            if len(comp) != len(valores_columnas):
                st.error("La entrada no tiene la longitud correcta. Asegúrate de seguir el formato especificado.")
            else:
                # Continuar con el procesamiento
                pass
        except ValueError:
            st.error("Error al convertir la entrada a números enteros. Asegúrate de ingresar valores numéricos válidos.")
        except Exception as e:
            st.error(f"Ocurrió un error inesperado: {str(e)}")

        inicio2 = time.time()
        MatrizOriginalEstados = list(matrixoriginalstates[0])
        indexEstado = MatrizOriginalEstados.index(comp)
        contenidoGraficar = MatrizOriginal[0][indexEstado]
        matrix_str = [''.join(map(str, sublist)) for sublist in matrixoriginalfirsttitle[0]]
        P.append(contenidoGraficar)
        resultado_original = contenidoGraficar
        ci, cj = 0, 0
        resultados_graficas = []

        while ci < len(combinacionesMatriz):
            matriz1 = combinacionesMatriz[ci][cj]
            matriz2 = combinacionesMatriz[ci][cj+1]
            matriz1 = converEstado2(vector, matriz1)[2:]
            matriz2 = converEstado2(vector, matriz2)[2:]
            
            if not isinstance(matriz1, list):
                matriz1 = [matriz1]
            if not isinstance(matriz2, list):
                matriz2 = [matriz2]

            A = np.array(matriz1)
            B = np.array(matriz2)
            
            if A.ndim != 2:
                A = A.reshape((1, -1))
            if B.ndim != 2:
                B = B.reshape((1, -1))
            
            res = MatricesKronecker([A, B])
            lista_resultados = res.tolist()
            lista_resultados_nueva = [[round(num, 2) for num in sublist[i:i+len(matrix_str)]] for sublist in lista_resultados for i in range(0, len(sublist), len(matrix_str))]
            contenidoGraficar = lista_resultados_nueva[indexEstado]
            resultados_graficas.append(contenidoGraficar)
            ci += 1
        fin2 = time.time()
        tiempo_transcurrido_2 = fin2 - inicio2

        inicio3 = time.time() 
        resultadosEMD = []
        for i in range(1, len(resultados_graficas)):
            resultadosEMD.append(earth_movers_distance(resultado_original, resultados_graficas[i]))

        combinations = []
        for combinacion in combinacionesMatriz[1:]:
            combinations.append(combinacion[0] + combinacion[1])

        min_index = np.argmin(resultadosEMD)
        min_emd = resultadosEMD[min_index]
        combinacionMinima = combinations[min_index]

        actualizar_etiqueta(min_emd, combinacionMinima)
        min_graf = resultados_graficas[min_index + 1]
        P.append(min_graf)
        graficarTablas(matrix_str, P)
        fin3 = time.time()
        tiempo_transcurrido_3 = fin3 - inicio3
        tiempo_total = tiempo_transcurrido_3 + tiempo_transcurrido_2 + tiempo_transcurrido_1
        st.write(f"Tiempo de ejecución de marginalización: {tiempo_total} segundos")

#---------------------------------------------------Interfaz principal---------------------------------------------------#
def main():
    global matriz
    global vector
    if 'vector' not in st.session_state:
        st.session_state.vector = None
    colB, colA = st.columns([8,2])
    with colA:
        st.image("Logo_de_la_Universidad_de_Caldas.svg.png", width=80)

    with colB:    
        st.title('PROYECTO FINAL ANÁLISIS')

    # Cargador de archivos
    archivo = st.file_uploader("Seleccionar archivo txt", type=['txt'])

    # Campo de texto para entrada manual
    texto_manual = st.text_area("O ingresa el texto aquí:")

    # Procesar la entrada
    if archivo is not None:
        matriz = leer_matriz_desde_texto(archivo.read().decode('utf-8'))
    
    elif texto_manual:
        matriz = leer_matriz_desde_texto(texto_manual)

    # Mostrar la matriz procesada
    if matriz:
        st.write(f"Matriz leída con éxito ({len(matriz)} filas)")

    if 'vista_actual' not in st.session_state:
        st.session_state.vista_actual = None

    col1, col2, col3, col4, col5 = st.columns([2,2,2.2,1.8,2])

    if col1.button("Mostrar matriz", key="btn_mostrar_matriz"):
        st.session_state.vista_actual = "Mostrar matriz"
    if col2.button("Estado futuro", key="btn_estado_futuro"):
        st.session_state.vista_actual = "Estado futuro"
    
    if col3.button("Marginalizacion", key="btn_marginalizacion"):
        st.session_state.vista_actual = "Marginalizacion"
    if col4.button("EMD", key="btn_emd"):
        st.session_state.vista_actual = "EMD"

    if st.session_state.vista_actual == "Marginalizacion":
        Marginalizacion(st.session_state.vector)
    elif st.session_state.vista_actual == "Mostrar matriz":
        MostrarMatriz(matriz)
    elif st.session_state.vista_actual == "Estado futuro":
        EstadoEstado(matriz)
    elif st.session_state.vista_actual == "Estado Canal":
        EstadoCanal(matriz)
    elif st.session_state.vista_actual == "EMD":
        EMD(st.session_state.vector)    
    elif st.session_state.vista_actual == None:
        limpiar()

main()
