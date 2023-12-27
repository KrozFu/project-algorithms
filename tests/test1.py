from pyemd import emd
import numpy as np

first_signature = np.array([0.0, 1.0])
second_signature = np.array([5.0, 3.0])
distance_matrix = np.array([[0.0, 0.5], [0.5, 0.0]])
emd = emd(first_signature, second_signature, distance_matrix)

print(emd)