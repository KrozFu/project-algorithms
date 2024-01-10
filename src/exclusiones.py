from difflib import ndiff
from itertools import product


def ExcluirFuturo(Elementos,Porcentajes):
    differences = list(ndiff(Elementos, 'ABC'))   
    differences = [diff[2:] for diff in differences if diff.startswith('-') or diff.startswith('+')]

    if len(differences)==1:
        return(ExcluirunFuturo(differences,Porcentajes))
    else:
        return(ExcluirunosFuturos(differences,Porcentajes))


def ExcluirunFuturo(Futuro,Porcentajes):
    Futuros={}
    if Futuro[0] == 'A':
        for Key,value in Porcentajes.items():
            Futuros[Key]=[]
            posicion=0
            for i in range(0, len(value), 2):
                Futuros[Key].append(value[i]+value[i+1])
                if(posicion==0):
                    posicion = 1
                else:
                    posicion=0

    elif Futuro[0] == 'B':
        for Key,value in Porcentajes.items():
            Futuros[Key]=[]
            for i in range(round(len(value)/2)):
                if(i<2):
                    Futuros[Key].append(value[i]+value[i+2])
                else:
                    Futuros[Key].append(value[i+2]+value[i+4])
    elif Futuro[0] == 'C':
        for Key,value in Porcentajes.items():
            Futuros[Key]=[]
            posicion=0
            for i in range(round(len(value)/2)):
                Futuros[Key].append(value[i]+value[i+4])
    return(Futuros)

def ExcluirunosFuturos(elemento,tabla):
    
    Futuros={}
    if elemento == ['A','B']:

        for Key,value in tabla.items():
            Futuros[Key]=[0,0]
            posicion =0
            for x in value:
                if(posicion < 4):
                    Futuros[Key][0]+=x
                else:
                    Futuros[Key][1]+=x
                posicion+=1





    elif elemento == ['A','C']:
        posicion=0
        for Key,value in tabla.items():
            Futuros[Key]=[0,0]
            for i in range(0, len(value), 2):
                Futuros[Key][posicion]+=value[i]+value[i+1]
                if(posicion==0):
                    posicion = 1
                else:
                    posicion=0





    elif elemento == ['B','C']:
        for Key,value in tabla.items():
            Futuros[Key]=[0,0]
            posicion =0
            for x in value:
                if(posicion%2==0):
                    Futuros[Key][0]+=x
                else:
                    Futuros[Key][1]+=x
                posicion+=1
    return(Futuros)



def ExcluirPresente(Porcentajes,Futuros,Presentes,ValorPresente):
    ExclusionFuturos={}
    Multiplicacion={}
    Retorno={}
    for x in Futuros:
        ExclusionFuturos[x]=ExcluirFuturo(x,Porcentajes)
    for key,value in ExclusionFuturos.items():
        Retorno[key]={}
        if(len(Presentes)==1):
            Retorno[key]=ExclusionFuturos[key]=ExcluirVariosPresentes(key,Presentes,value)
        else:
            Retorno[key]=ExclusionFuturos[key]=ExcluirUnPresente(key,Presentes,value)
    for x,y in Retorno.items():
        Multiplicacion[x]=Retorno[x][ValorPresente]
    if(len(Retorno)>1):
        return(Multiplicar(Multiplicacion))
    else:
        return(Retorno[Futuros][ValorPresente])


def ExcluirUnPresente(llave,presente,valores):
    Retorno={}
    differences = list(ndiff(presente, 'ABC'))
    differences = [diff[2:] for diff in differences if diff.startswith('-') or diff.startswith('+')]
    # print("Excluire a "+str(presente)+" De los valores "+str(differences))
    if differences[0]=='A':
        for Key,value in valores.items():
            if(not(Key[1:3] in Retorno)):
                Retorno[Key[1:3]]=[]
                i = 0
                while i < len(valores):
                    SKey, Svalue = list(valores.items())[i]
                    if Key[1:3] == SKey[1:3] and Key != SKey:
                        Retorno[Key[1:3]].append((Svalue[0] + value[0]) / 2)
                        Retorno[Key[1:3]].append((Svalue[1] + value[1]) / 2)
                        i = len(valores)  # Termina el bucle cuando se cumple la condición
                    else:
                        i += 1

    elif differences[0]=='B':
        for Key,value in valores.items():
            if(not(str(Key[0])+str(Key[-1]) in Retorno)):
                Retorno[str(Key[0])+str(Key[-1])]=[]
                i = 0
                while i < len(valores):
                    SKey, Svalue = list(valores.items())[i]
                    if str(Key[0])+str(Key[-1]) == str(SKey[0])+str(SKey[-1]) and Key != SKey:
                        Retorno[str(Key[0])+str(Key[-1])].append((Svalue[0] + value[0]) / 2)
                        Retorno[str(Key[0])+str(Key[-1])].append((Svalue[1] + value[1]) / 2)
                        i = len(valores)  # Termina el bucle cuando se cumple la condición
                    else:
                        i += 1

    elif differences[0]=='C':
        for Key,value in valores.items():
            if(not(Key[0:2] in Retorno)):
                Retorno[Key[0:2]]=[]
                i = 0
                while i < len(valores):
                    SKey, Svalue = list(valores.items())[i]
                    if Key[0:2] == SKey[0:2] and Key != SKey:
                        Retorno[Key[0:2]].append((Svalue[0] + value[0]) / 2)
                        Retorno[Key[0:2]].append((Svalue[1] + value[1]) / 2)
                        i = len(valores)  # Termina el bucle cuando se cumple la condición
                    else:
                        i += 1

    return(Retorno)


#Cuanto se ingresa una sola variable de presente se excluyen varios esta funcion se encarga de eso
def ExcluirVariosPresentes(llave,presentes,valores):
    Retorno={}
    differences = list(ndiff(presentes, 'ABC'))
    differences = [diff[2:] for diff in differences if diff.startswith('-') or diff.startswith('+')]
    return(AutomatizacionVP(Retorno,valores,ord(presentes.lower()) - 97))


def AutomatizacionVP(Retorno,valores,Posicion):
    llaves = {"0": [], "1": []}
    for Key,value in valores.items():
        if Key[Posicion] not in Retorno:
            Retorno[Key[Posicion]] = [0, 0]
        found_match = False
        i = 0
        while i < len(valores) and not found_match:
            SKey, SValue = list(valores.items())[i]
            if Key[Posicion] == SKey[Posicion] and SKey not in llaves[Key[Posicion]]:
                llaves[Key[Posicion]].append(SKey)
                Retorno[Key[Posicion]][0] += SValue[0]
                Retorno[Key[Posicion]][1] += SValue[1]
                found_match = True
            i += 1
    for llave,recursos in Retorno.items():
        Retorno[llave][0]=Retorno[llave][0]/4
        Retorno[llave][1]=Retorno[llave][1]/4
    return(Retorno)

def Multiplicar(Multiplicadores):
    tabla= []

    # Imprime arrego de las multiplicaciones
    # print(Multiplicadores)

    for x,y in  Multiplicadores.items():
        tabla.append(Multiplicadores[x])
    if(len(tabla)==3):
        combinaciones = list(product(*tabla))
        resultados = [round(prod[0] * prod[1] * prod[2], 2)/10000 for prod in combinaciones]
        return resultados
    else:
        resultados = [round((x * y), 2) for x in tabla[0] for y in tabla[1]]

        for x in range(len(resultados)):
            resultados[x]=resultados[x]/100
        return resultados

def PresenteCero(Futuro):
    Resultados ={}
    Final = []
    for x in range(len(Futuro['000'])):
        Resultados[str(x)] = 0
    for x in Futuro:
        for y in range(len(Futuro[x])):
            Resultados[str(y)] += Futuro[x][y]
    for x in Resultados:
        Resultados[str(x)] = Resultados[x]/8
        Final.append(Resultados[str(x)])
    return Final



def FuturoCero(Presente):
    resultados = {clave: sum(valores) for clave, valores in Presente.items()}
    final = []
    for x in resultados:
        final.append(resultados[str(x)])
    return final


def EMD(Primera,Segunda):
    emd = 0
    for x in range(len(Primera)):
        if Primera[x] !=0:
            if Primera[x] > Segunda[x]:
                emd += Primera[x]*0.01 - Segunda[x]*0.01
            elif Segunda[x] > Primera[x]:
                emd += Segunda[x]*0.01 - Primera[x]*0.01
    return emd


def reducir_diccionario(diccionario, val_presente):
    nuevos_items = {'0': [0.0] * len(diccionario['000']),
                    '1': [0.0] * len(diccionario['000'])}

    for clave, valores in diccionario.items():
        if clave[val_presente] == "0":
            nuevos_items['0'] = [nuevos_items['0'][i] + valores[i] for i in range(len(valores))]
        elif clave[val_presente] == "1":
            nuevos_items['1'] = [nuevos_items['1'][i] + valores[i] for i in range(len(valores))]

    return nuevos_items