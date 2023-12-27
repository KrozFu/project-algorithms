# Declarar las variables
vector1 = []
vector2 = []

# Leer la cadena de texto para el vector 1
cadena1 = input("Ingrese una cadena de texto para el vector 1: ")
vector1.extend(['0'] + list(cadena1))

# Leer la cadena de texto para el vector 2
cadena2 = input("Ingrese una cadena de texto para el vector 2: ")
vector2.extend(['0'] + list(cadena2))

# Imprimir los vectores de entrada
print("Vector 1:", vector1)
print("Vector 2:", vector2)
