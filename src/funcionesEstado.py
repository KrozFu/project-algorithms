import pandas as pd
import src.exclusiones as E
import re
from itertools import product
import queue

val_alfa = {
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

def EstadoCanalF(Array,Posiciones,tam):
    my_dic = {}
    listas = []
    #Se genera un Array con el numero de entradas la cantidad de estados posibles
    for x in range(tam):
        listas.append([[] for _ in range(len(Posiciones))])

    for x in range(len(Posiciones)):      
        y = 0
        #Se le ingresa a cada uno de los elementos un estado en el numero de entradas
        for z in range(tam):
            listas[z][x].append(Posiciones[x][0])
        #Se recorre todos los elementos excepto el ultimo elemento ya que el ultimo elemento no puede tener estado futuro
        while y < len(Posiciones[x])-1 and Posiciones[x][y+1] != len(Array[0]):
            #Se recoore todos las entradas
            for i in range(tam):
                # se le ingresa el valor siquiente del canal i para cada estado
                listas[i][x].append(Array[i][Posiciones[x][y+1]])
            y +=1

    #se genera un diccioonario con la letra correspondiente de cada entrada 
    for i in range(len(listas)):
        my_dic[chr(i + 65)]=listas[i]

    PorporFutu_Dict = {}

    for key, value in my_dic.items():
        proporciones = []
        for sublist in value:
            Elementos = len(sublist) - 1  # Restamos 1 para no contar el primer elemento
            total_unos = sum(sublist[1:])  # Sumamos todos los unos en la sublista
            proporcion = total_unos / Elementos if Elementos > 0 else 0  # Evitamos la división por cero
            proporciones.append([sublist[0], proporcion])
        PorporFutu_Dict[key] = proporciones
    # Crear un DataFrame a partir del diccionario
    df = pd.DataFrame({key: [val[1] for val in value] for key, value in PorporFutu_Dict.items()}, index=[val[0] for val in next(iter(PorporFutu_Dict.values()))])

    # Renombrar las columnas con los nombres de las claves
    df.columns = PorporFutu_Dict.keys()

    # print(df)
    return(PorporFutu_Dict)
# --------------------------------------------------------------------------------

#Punto 2
def EstadoEstadoF(Array,Posiciones,Estados):
    Estados=[["Estado",]]
    for x in range(len(Posiciones)):
        Estados[0].append(Posiciones[x][0])
        Estados.append([Posiciones[x][0]])
    for x in range(len(Posiciones)):
        y=1
        while y<len(Posiciones[x]):
            if Posiciones[x][y] != len(Array[0]):
                agregacion = ""
                for z in range(len(Array)):
                     agregacion+=str(Array[z][Posiciones[x][y]])
                Estados[x+1].append(agregacion)
            y+=1

    my_dic={}
    for fila in Estados:
        estado = fila[0]  
        valores = fila[1:]  
        my_dic[estado] = valores

    diccionario_normalizado_porcentaje = {}

    for clave, lista_elementos in my_dic.items():
        if clave != 'Estado' and len(my_dic[clave]) !=0:
            total_estado = len(my_dic[clave])
            valores_normalizados_porcentaje = [(lista_elementos.count(elemento) / total_estado) * 100 for elemento in my_dic['Estado']]
            # valores_normalizados_porcentaje = [(lista_elementos.count(elemento) / total_estado) for elemento in my_dic['Estado']]
            diccionario_normalizado_porcentaje[clave] = valores_normalizados_porcentaje

    # for x in diccionario_normalizado_porcentaje.keys():
    #     print(x+str(diccionario_normalizado_porcentaje[x]))
    
    return diccionario_normalizado_porcentaje

# --------------------------------------------------------------------------------
# Punto 3
def EstadoCanalP(Array,Posiciones,tam):
    my_dic = {}
    listas = []
    for x in range(tam):
        listas.append([[] for _ in range(len(Posiciones))])
    for x in range(len(Posiciones)):      
        y = 2
        for z in range(tam):
            listas[z][x].append(Posiciones[x][0])
        while y < len(Posiciones[x])+1:
            if(Posiciones[x][y-1]!=1):
                for i in range(tam):
                    listas[i][x].append(Array[i][Posiciones[x][y-1]-2])
            else:
                for i in range(tam):
                    listas[i][x].append(0)
            y +=1
    for i in range(len(listas)):
        my_dic[chr(i + 65)]=listas[i]

    proporcion_dict = {}

    for key, value in my_dic.items():
        proporciones = []
        for sublist in value:
            total_elementos = len(sublist) - 1  # Restamos 1 para no contar el primer elemento
            total_unos = sum(sublist[1:])  # Sumamos todos los unos en la sublista
            proporcion = total_unos / total_elementos if total_elementos > 0 else 0  # Evitamos la división por cero
            proporciones.append([sublist[0], proporcion])
        proporcion_dict[key] = proporciones

    df = pd.DataFrame({key: [val[1] for val in value] for key, value in proporcion_dict.items()}, index=[val[0] for val in next(iter(proporcion_dict.values()))])

    df.columns = proporcion_dict.keys()
    
    return(proporcion_dict)
    

# --------------------------------------------------------------------------------
# Punto 4
def EstadoEstadoP(Array,Posiciones,elementos):
    Estados=[["Estado",]]
    for x in range(len(Posiciones)):
        Estados[0].append(Posiciones[x][0])
        Estados.append([Posiciones[x][0]])

    for x in range(len(Estados)-1):
        y=0
        if y==len(Posiciones[x])-1:
            for x in range(len(Estados)-1):
                Estados[x+1].append(0.0)
        while y<len(Posiciones[x])-1 and  Posiciones[x][y+1] != 30:
            agregacion="";
            for z in range(len(Array)):
                agregacion+=str(Array[z][Posiciones[x][y+1]])
            Estados[x+1].append(agregacion)
            y+=1;
    my_dic={}
    for fila in Estados:
        estado = fila[0]  
        valores = fila[1:]  
        my_dic[estado] = valores
    diccionario_normalizado_porcentaje = {}

    for clave, lista_elementos in my_dic.items():
        if clave != 'Estado' and len(my_dic[clave]) !=0:
            total_estado = len(my_dic[clave])
            valores_normalizados_porcentaje = [(lista_elementos.count(elemento) / total_estado) * 100 for elemento in my_dic['Estado']]
            # valores_normalizados_porcentaje = [(lista_elementos.count(elemento) / total_estado) for elemento in my_dic['Estado']]
            diccionario_normalizado_porcentaje[clave] = valores_normalizados_porcentaje

    # for x in diccionario_normalizado_porcentaje.keys():
    #     print(x+str(diccionario_normalizado_porcentaje[x]))
    
    return(diccionario_normalizado_porcentaje)
    
#Division De elemento
def DivisionElementos(Operacion,Porcentajes):
    Operacion = Operacion.split("/")
    ElementosFuturos= Operacion[0]

    # print(Operacion)
    
    if(Operacion[1]!=str(0) and Operacion[0]!=str(0)):
        ElementosPresente=Operacion[1].split("=")[0]
        ValorPresente=Operacion[1].split("=")[1]
    else:
        ElementosPresente = Operacion[1]
        ValorPresente = Operacion[1]
    #print("Presente = "+ElementosPresente+", Valor = "+ValorPresente+", Futuro = "+ElementosFuturos)
    Casos = {}
    if(len(ElementosPresente)==3 and len(ElementosFuturos)==3):
        #print(Porcentajes[ValorPresente])
        #print(Porcentajes)
        return(Porcentajes[ValorPresente])
    else:

        #print(ElementosFuturos+' / '+ElementosPresente)
        if(ElementosPresente == str(0)):
            if(len(ElementosFuturos)==3):
                return(E.PresenteCero(Porcentajes))
            else:
                Final=E.ExcluirFuturo(ElementosFuturos,Porcentajes)
                # print(Final)

                return(E.PresenteCero(Final))

        
        # Entrada para evaluar futuro vacio
        elif(ElementosFuturos == str(0)):
            val_llave = ElementosPresente.split("=")[1]
            ElementosPresente = ElementosPresente.split("=")[0]

            # Estalla por usar dos variables cuando el futuro es 0
            if len(ElementosPresente) == 1:
                val_presente = val_alfa[ElementosPresente]
                diccionario_resultante = E.reducir_diccionario(Porcentajes,val_presente)
                resultado = E.FuturoCero(diccionario_resultante,val_llave)
            else:
                val = [100.0]
                resultado = val
            
            return resultado


        elif(len(ElementosFuturos)!=3 and len(ElementosPresente)==3):
            Casos=E.ExcluirFuturo(ElementosFuturos,Porcentajes)
            #print(Casos[ValorPresente])
            return(Casos[ValorPresente])
        elif(len(ElementosPresente)!=3):
            Final=E.ExcluirPresente(Porcentajes,ElementosFuturos,ElementosPresente,ValorPresente)
            #print(Final)
            return(Final)
        else:
            #print(Casos[ValorPresente])
            return(Casos[ValorPresente])


def tratamiento(cadena):
    nueva_cadena = re.sub(r'0(?=[A-Za-z])', '', cadena)
    return nueva_cadena

def generar_combinaciones(vector1, vector2, estado):
    # Extraer el resultado de la división y convertir los caracteres según el diccionario
    def calcular_resultado(caso):
        res = caso.split("/")[1]
        if res != "0":
            resultado_val = ''.join(dic_val_presentes.get(caracter, '') for caracter in res)
            caso = f"{caso}={resultado_val}"
        return caso
    
    combinaciones = {}
    contador = 0

    dic_val_presentes = dict(zip(''.join(vector2[1:]), estado))

    for elem1, elem2 in product(vector1, vector2):
        if elem1 == '0' and elem2 == '0':
            continue

        combinacion1 = f'{elem1}/{elem2}'
        combinacion2 = f'{"".join([x for x in vector1 if x != elem1])}/{"".join([x for x in vector2 if x != elem2])}'

        combinaciones[contador] = [combinacion1, tratamiento(combinacion2)]
        contador += 1

    for i, elem1 in enumerate(vector1):
        combinacion1 = f'{elem1}/{"".join(vector2[1:])}'
        combinacion2 = f'{"".join(vector1[:i] + vector1[i+1:])}/{"".join(vector2[0])}'

        combinaciones[contador] = [combinacion1, tratamiento(combinacion2)]
        contador += 1

    resultado_final_combinaciones = {llave: [calcular_resultado(caso) for caso in valores] for llave, valores in combinaciones.items()}
    return resultado_final_combinaciones


def calculo_emd_funcion(caso1, caso2, porcentajes, resultados):
    primero = DivisionElementos(caso1, porcentajes)
    segundo = DivisionElementos(caso2, porcentajes)
    multiplicacion = {'A': primero, 'B': segundo}

    print(primero)
    print(segundo)
    
    distancia = E.EMD(resultados, E.Multiplicar(multiplicacion))

    return distancia

def solucion(valores, porcentajes, resultado_caso_general):
    mejor_solucion = calculo_emd_funcion(valores[0], valores[1], porcentajes, resultado_caso_general)
    return mejor_solucion

def solucion_minima(vector1, vector2, estado, porcentajes):
    # Crear el caso base
    caso_general = f"{''.join(vector1[1:])}/{''.join(vector2[1:])}={estado}"
    
    # Calcular la división de los elementos y mostrar el cago general
    resultado_caso_general = DivisionElementos(caso_general, porcentajes)

    # Inicializar la cola de prioridad
    cola_prioridad = queue.PriorityQueue()
    # Agregar el caso base a la cola de prioridad
    cola_prioridad.put((0, vector1, vector2, resultado_caso_general))

    while not cola_prioridad.empty():
        # Obtener el próximo elemento de la cola de prioridad
        _, v1, v2, res = cola_prioridad.get()

        # Generar combinaciones de casos
        combinaciones = generar_combinaciones(v1, v2, estado)

        for llave, valores in combinaciones.items():
            nueva_solucion = solucion(valores, porcentajes, res)
            
            if nueva_solucion == 0:
                # print(f'EMD={nueva_solucion}')
                return nueva_solucion  # Se encontró una solución, terminar

            # Calcular una cota inferior para la solución actual
            cota_inferior = nueva_solucion
            # Agregar la combinación a la cola de prioridad con la cota inferior como prioridad
            cola_prioridad.put((cota_inferior, valores[0], valores[1], DivisionElementos(llave, porcentajes)))

    # Si se llega aquí, no se encontró una solución con distancia cero
    return None


def posibles_soluciones(vector1, vector2, estado, porcentajes):
    # Crear el caso base
    caso_general = f"{''.join(vector1[1:])}/{''.join(vector2[1:])}={estado}"
    
    # Calcular la división de los elementos y mostrar el cago general
    resultado_caso_general = DivisionElementos(caso_general, porcentajes)
    print("Caso Base")
    print(resultado_caso_general)
    print("-----------------------------------------------------------")

    # Generar combinaciones de casos
    combinaciones = generar_combinaciones(vector1, vector2, estado)
    # print(combinaciones)

    for llave, valores in combinaciones.items():
        mejor_solucion = solucion(valores, porcentajes, resultado_caso_general)
        print(f'EMD={mejor_solucion}')
        print("-----------------------------------------------------------")
