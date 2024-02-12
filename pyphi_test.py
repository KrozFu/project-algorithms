import pyphi
import numpy as np
import time

def solucion_pyphi():
    start_time = time.time()

    with open("data/data.txt") as archivo:
        data_array = np.array([linea.split(",") for linea in archivo.read().splitlines()])


    print(data_array)

    network = pyphi.Network(data_array, node_labels=['A','B','C','D','E','F'])

    state = (1,0,0,0,1,0)
    nodes = ('A','B','C','D','E','F')
    subsystem = pyphi.Subsystem(network,state,nodes)

    A,B,C,D,E,F = subsystem.node_indices
    purview = (A,B,C) # Futuro
    mechanism = (A,B,C) # Presente
    mip = subsystem.effect_mip(mechanism, purview)

    print(f"MIP: {mip}")

    end_time = time.time()
    print(f"Tiempo de ejecución: {end_time - start_time}")

solucion_pyphi()
