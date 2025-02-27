import os
import sys
import re
import numpy as np
import matplotlib.pyplot as plt

import ctypes

def get_point_formulas(input_symmetry : str) -> list[str]:
    lines = []

    # Changes working directory and then goes back
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    with open("Data/wyckoff_positions_2D_Letters.txt") as data:
        lines = [line.strip() for line in data]
    os.chdir("test")
    
    # Formatting input data
    symmetry_info = list(filter(None, re.split(r'(\d+)', input_symmetry)))
    letters = list(symmetry_info[1])
    axis_formulas = []

    for i in range(len(lines)):
        if(lines[i][0:4] == f"# {symmetry_info[0]}"):
            # Go until you find all letters
            for j in range(1, len(lines)-i):
                if(len(letters) == 0):
                    break
                if(lines[i+j][0] in letters):
                    axis_formulas.append(lines[i+j])
                    letters.remove(lines[i+j][0])

    return axis_formulas

def extract_parentheses(axis_formulas : str) -> str:
    return [match.strip('()') for match in re.findall(r"\(.*?\)", axis_formulas)]

def calculate_discrepancies(symmetry_name : str, resolution : int):
    # Formatting to get all of the points
    
    point_formulas = get_point_formulas(symmetry_name)
    individual_formulas = [extract_parentheses(point_formulas[i]) for i in range(len(point_formulas))]
    all_points = []
    [all_points.extend(element) for element in individual_formulas]
    
    # Prepare to parse to C file
    
    all_points_bytes = []
    for i in range(len(all_points)):
        all_points_bytes.append(bytes(all_points[i], "utf-8"))
    all_points_array = (ctypes.c_char_p * (len(all_points_bytes)+1))()
    all_points_array[:-1] = all_points_bytes
    
    # Find the shared library
    path = os.getcwd()

    try:
        heatmap_calculation_clibrary = ctypes.CDLL(os.path.join(path, "heatmap_calculation.dll"))
    except(FileNotFoundError):
        # os.system writes to terminal
        os.system("gcc -fPIC -shared -o heatmap_calculation.dll heatmap_calculation.c")
        heatmap_calculation_clibrary = ctypes.CDLL(os.path.join(path, "heatmap_calculation.dll"))
        
    heatmap_calculation_clibrary.discrepancy_calculation.restype = ctypes.POINTER(ctypes.c_double)
    discrepancies = ctypes.POINTER(ctypes.c_double)
    discrepancies = heatmap_calculation_clibrary.discrepancy_calculation(all_points_array, len(all_points), resolution)
    # Free memory
    heatmap_calculation_clibrary.free_discrepancies.argtypes = [ctypes.POINTER(ctypes.c_double)]
    heatmap_calculation_clibrary.free_discrepancies(discrepancies)
    
    discrepancies_list = []

    # Temporary solution to memory leaks
    for i in range(0, resolution**2):
        if(discrepancies[i] >= 0 and discrepancies[i] <= 1):
            discrepancies_list.append(discrepancies[i])
        else:
            discrepancies_list.append(discrepancies[i-1])
    
    return discrepancies_list
    
def plot_heatmap(symmetry_name : str, resolution : int = 100, create_pdf_files : bool = False) -> None:
    plt.clf()
    
    discrepancies = calculate_discrepancies(symmetry_name, resolution)

    heatmap_data = np.array(discrepancies).reshape(resolution, resolution) 

    # "hot" also works 
    plt.imshow(heatmap_data, cmap='seismic', aspect='auto', extent=[0, 1, 0, 1], origin='lower', interpolation='gaussian')
    plt.colorbar(label=f'D* (Max : {max(discrepancies)})')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(symmetry_name)
    
    if(create_pdf_files):
        plt.savefig(f'{symmetry_name}.pdf')
    else:
        plt.show()
    
    plt.close()

if(__name__ == "__main__"):
    print(plot_heatmap("17ed"))