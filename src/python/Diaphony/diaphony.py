import sys
import os
import math
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__),'../'))

from Star_Discrepancy.pointset_generators import generate_halton_sequence_points

def e_h(x_vector : list, h_vector : list):
    return np.exp(complex(0,2*math.pi * sum(i*j for (i, j) in zip(x_vector, h_vector))))
    
def S_N(pointset, h_vector):
    n = len(pointset)
    value = 0
    for j in range(n):
        value += e_h(pointset[j], h_vector)
    
    return 1/n * value

def r(h_vector : list[int]) -> float:
    d = len(h_vector)
    value = 1
    for j in range(d):
        value *= max(1, abs(h_vector[j]))
    return value

def Zinterhof_Diaphony(pointset : list[list[float]], lower_bound : int = -10, upper_bound : int = 10) -> float:
    value = 0

    for h in range(lower_bound, upper_bound + 1):
        for k in range(lower_bound, upper_bound + 1):
            for l in range(lower_bound, upper_bound + 1):
                h_vector = [h,k,l]
                if(h_vector == [0,0,0]):
                    pass
                else:
                    value += (abs(S_N(pointset, h_vector)))**2 * (r(h_vector))**-2
    temp = 1 / ((1 + np.pi**2 / 3)**3 - 1)
    return math.sqrt(temp*value)

if __name__ == "__main__":
    pointset = generate_halton_sequence_points(10, 3)
    diaphony_value = Zinterhof_Diaphony(pointset)
    print(diaphony_value)