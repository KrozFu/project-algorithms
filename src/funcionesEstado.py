import pandas as pd
import src.exclusiones as E

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
    print(Operacion)
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
            val_presente = val_alfa[ElementosPresente]
            diccionario_resultante = E.reducir_diccionario(Porcentajes,val_presente)
            # print(E.FuturoCero(diccionario_resultante))

            return(E.FuturoCero(diccionario_resultante))


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
