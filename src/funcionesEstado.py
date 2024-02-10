import pandas as pd
import src.exclusiones as E
import re
from itertools import product

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
    def calcular_resultado(caso):
        res = caso.split("/")[1]
        if res != "0":
            resultado_val = ''.join(dic_val_presentes.get(caracter, '') for caracter in res)
            caso = f"{caso}={resultado_val}"
        return caso
    
    combinaciones_set = set()

    dic_val_presentes = dict(zip(''.join(vector2[1:]), estado))

    def agregar_combinacion(elem1, elem2):
        combinacion1 = f'{elem1}/{elem2}'
        combinacion2 = f'{"".join([x for x in vector1 if x != elem1])}/{"".join([x for x in vector2 if x != elem2])}'

        combinacion = [combinacion1, tratamiento(combinacion2)]
        return combinacion

    for elem1, elem2 in product(vector1, vector2):
        if elem1 == '0' and elem2 == '0':
            continue

        combinacion = agregar_combinacion(elem1, elem2)
        combinacion.sort()  # Ordenar las cadenas dentro de la combinación
        if '0/0' not in combinacion:
            combinaciones_set.add(tuple(combinacion))

    for i, elem1 in enumerate(vector1):
        if elem1 == '0':
            continue

        combinacion1 = f'{elem1}/{"".join(vector2[1:])}'
        combinacion2 = f'{"".join(vector1[:i] + vector1[i+1:])}/{"".join(vector2[0])}'

        combinacion = [combinacion1, tratamiento(combinacion2)]
        combinacion.sort()

        if '0/0' not in combinacion:
            combinaciones_set.add(tuple(combinacion))

   
    resultado_final_combinaciones = {i: [calcular_resultado(caso) for caso in combinacion] for i, combinacion in enumerate(combinaciones_set)}

    # print(resultado_final_combinaciones)

    # resultado_final_combinaciones = {0: ['0/C=0', 'ABC/A=1'], 1: ['C/C=0', 'AB/A=1'], 2: ['A/0', 'BC/AC=10'], 3: ['A/A=1', 'BC/C=0'], 4: ['A/C=0', 'BC/A=1'], 5: ['B/0', 'AC/AC=10'], 6: ['B/A=1', 'AC/C=0'], 7: ['B/C=0', 'AC/A=1'], 8: ['C/0', 'AB/AC=10'], 9: ['C/A=1', 'AB/C=0'], 10: ['0/A=1', 'ABC/C=0'], 11: ['0/AC=10', 'ABC/0'], 12: ['A/AC=10', 'BC/0'], 13: ['B/AC=10', 'AC/0'], 14: ['C/AC=10', 'AB/0']}
    # resultado_final_combinaciones = {0: ['C/A=1', 'AB/C=0']}
    # resultado_final_combinaciones = {0: ['0/A=1', 'ABC/C=0']} # --> Caso funcional
    
    return resultado_final_combinaciones


def calculo_emd_funcion(caso1, caso2, porcentajes, resultados):
    primero = DivisionElementos(caso1, porcentajes)
    segundo = DivisionElementos(caso2, porcentajes)
    # print(primero)
    # print(segundo)

    multiplicacion = {'A': primero, 'B': segundo} 
    distancia = E.EMD(resultados, E.Multiplicar(multiplicacion))

    return distancia, primero, segundo

def solucion(valores, porcentajes, resultado_caso_general):
    mejor_solucion, primero, segundo = calculo_emd_funcion(valores[0], valores[1], porcentajes, resultado_caso_general)
    return mejor_solucion, primero, segundo

def solucion_minima(vector1, vector2, estado, porcentajes, limite_superior=float('inf')):
    # Crear el caso base
    caso_general = f"{''.join(vector1[1:])}/{''.join(vector2[1:])}={estado}"

    # Calcular la división de los elementos y mostrar el caso general
    resultado_caso_general = DivisionElementos(caso_general, porcentajes)

    # Generar combinaciones de casos
    combinaciones = generar_combinaciones(vector1, vector2, estado)

    for llave, valores in combinaciones.items():
        mejor_solucion, primero, segundo = solucion(valores, porcentajes, resultado_caso_general)
        # print(f'EMD={mejor_solucion}')
        # print("-----------------------------------------------------------")

        # Aplicar la técnica de poda
        if mejor_solucion == 0:
            data_dic = [caso_general, resultado_caso_general, valores[0], primero, valores[1], segundo]
            
            # print("Se alcanzó la mejor solución con EMD=0. Terminando el proceso.")
            return diccionario_grafica(data_dic)
        elif mejor_solucion < limite_superior:
            limite_superior = mejor_solucion
        else:
            print(f"Poda de rama. EMD={mejor_solucion} es mayor que el límite superior {limite_superior}.")
            continue


def posibles_soluciones(vector1, vector2, estado, porcentajes):
    # Crear el caso base
    caso_general = f"{''.join(vector1[1:])}/{''.join(vector2[1:])}={estado}"
    
    # Calcular la división de los elementos y mostrar el cago general   
    resultado_caso_general = DivisionElementos(caso_general, porcentajes)
    print(caso_general)
    print("Caso Base")
    print(resultado_caso_general)
    print("-----------------------------------------------------------")

    # Generar combinaciones de casos
    combinaciones = generar_combinaciones(vector1, vector2, estado)
    print(combinaciones)
    print("-----------------------------------------------------------")

    for llave, valores in combinaciones.items():
        mejor_solucion, primero, segundo = solucion(valores, porcentajes, resultado_caso_general)
        print(valores)
        print(f'EMD={mejor_solucion}')
        print("-----------------------------------------------------------")


def diccionario_grafica(data):
    result_dict = {}
    current_conjunto = None

    for i, item in enumerate(data):
        if '/' in item:
            # Se trata de una etiqueta general, crearemos un nuevo conjunto
            current_conjunto = f"conjunto_{i // 2 + 1}"
            result_dict[current_conjunto] = [{"caso": item}]
        else:
            # Se trata de valores, los agregaremos al conjunto actual
            result_dict[current_conjunto].append({"valores": item})

    # print(result_dict)
    return result_dict
