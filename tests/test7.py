import re

vector1 = ['0', 'A', 'B', 'C']
vector2 = ['0', 'A', 'C']

def tratamiento(cadena):
    nueva_cadena = re.sub(r'0(?=[A-Za-z])', '', cadena)
    return nueva_cadena

def imprimir_combinaciones(combinacion1, combinacion2):
    print("Combinación 1:", combinacion1)
    print("Combinación 2:", tratamiento(combinacion2))
    print("------------------------------------")

def generar_combinaciones(vector1, vector2):
    for elem1 in vector1:
        for elem2 in vector2:
            if elem1 == '0' and elem2 == '0':
                continue

            combinacion1 = f'{elem1}/{elem2}'
            combinacion2 = f'{"".join(vector1).replace(elem1, "")}/{"".join(vector2).replace(elem2, "")}'

            imprimir_combinaciones(combinacion1, combinacion2)

    for i in range(len(vector1)):
        combinacion1 = f'{vector1[i]}/{"".join(vector2[1:])}'
        combinacion2 = f'{"".join(vector1[:i] + vector1[i+1:])}/{"".join(vector2[0])}'

        imprimir_combinaciones(combinacion1, combinacion2)

# Generar combinaciones
generar_combinaciones(vector1, vector2)
