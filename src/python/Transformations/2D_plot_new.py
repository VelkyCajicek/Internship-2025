import sys
import os
import re
import numpy as np
import matplotlib.pyplot as plt

sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
from Star_Discrepancy.QMC.Bundschuh_Zhu import Bundschuh_Zhu_Algorithm
sys.path.append(os.path.join(os.path.dirname(__file__),'../../../'))

def get_point_formulas(input_symmetry : str) -> list[str]:
    lines = []
    
    with open("Data/wyckoff_positions_2D_Letters.txt") as data:
        lines = [line.strip() for line in data]
    
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

def generate_pointset(x_value : float, y_value : float, all_points : list[str]) -> list[list]:
    pointset = []

    for i in range(len(all_points)):
        coordinates = all_points[i].split(',')
        coordinates[0] = round(eval(str(coordinates[0]).replace('x', str(x_value)).replace('y', str(y_value))) % 1, 1)
        coordinates[1] = round(eval(str(coordinates[1]).replace('x', str(x_value)).replace('y', str(y_value))) % 1, 1)
        pointset.append([coordinates[0], coordinates[1]])

    return pointset

def remove_duplicates(pointset : list[list[float]]) -> list[list]:
    seen = set()
    unique_points = []
    
    for point in pointset:
        # Convert to tuple for hashability
        tuple_point = tuple(point)
        if tuple_point not in seen:
            seen.add(tuple_point)
            unique_points.append(point)
    
    return unique_points

def calculate_discrepancies(interpolations : int, symmetry_name : str) -> list[float]:
    discrepancies = []
    run_value = 0
    
    # Most of the remaining functions which are run
    
    point_formulas = get_point_formulas(symmetry_name)
    
    # May be temporary code
    try:
        if(("y" not in point_formulas[0] and "y" not in point_formulas[1]) or ("x" not in point_formulas[0] and "x" not in point_formulas[1])):
            point_formulas[1] = point_formulas[1].replace("x", "y")
    except(IndexError):
        pass
    
    individual_formulas = [extract_parentheses(point_formulas[i]) for i in range(len(point_formulas))]
    all_points = []
    [all_points.extend(element) for element in individual_formulas]
    
    # Calculates the D*
    
    for x in range(0, interpolations):
        for y in range(0, interpolations):
            poinset = generate_pointset(round(x / interpolations, 1), round(y / interpolations, 1), all_points)
            poinset = remove_duplicates(poinset)
            discrepancies.append(Bundschuh_Zhu_Algorithm(poinset))

            run_value += 1
            updt(interpolations**2, run_value)
    
    print("D* calculation finished; Creating heatmap ...")
    return discrepancies

def plot_heatmap(symmetry_name : str, interpolations : int = 100) -> None:
    plt.clf()
    
    discrepancies = calculate_discrepancies(interpolations, symmetry_name)

    heatmap_data = np.array(discrepancies).reshape(interpolations, interpolations) 

    # "hot" also works 
    plt.imshow(heatmap_data, cmap='seismic', aspect='auto', extent=[0, 1, 0, 1], origin='lower', interpolation='gaussian')
    plt.colorbar(label=f'D* (Max : {max(discrepancies)})')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(symmetry_name)
    
    plt.savefig(f'{symmetry_name}.pdf')
    # plt.show()
    
    plt.close()
    
def updt(total, progress) -> None:
    barLength, status = 20, ""
    progress = float(progress) / float(total)
    if progress >= 1.:
        progress, status = 1, "\r\n"
    block = int(round(barLength * progress))
    text = "\r[{}] {:.0f}% {}".format(
        "#" * block + "-" * (barLength - block), round(progress * 100, 0),
        status)
    sys.stdout.write(text)
    sys.stdout.flush()

def generate_examples():
    true_2_degrees_of_freedom = []
    lines = []
    
    with open("Data/wyckoff_positions_2D_Letters.txt") as data:
        lines = [line.strip() for line in data]
    
    for i in range(len(lines)):
        if(lines[i][0]) == "#":
            multiplicity = lines[i].replace("#", "").replace(" ", "")
            letter = lines[i+1][0:lines[i+1].index(":")].replace(" ", "")
            true_2_degrees_of_freedom.append(f"{multiplicity}{letter}")
    
    return true_2_degrees_of_freedom

def generate_heatmaps(input_symmetry_list : list[str]) -> None:
    # Function that gets all the first multiplicities
    #input_symmetry_list = generate_examples()
    
    for i in range(len(input_symmetry_list)):
        try:
            plot_heatmap(str(input_symmetry_list[i]))
        # ZeroDivisionError occurs in Bundschuh Zhu
        except(ZeroDivisionError):
            # Doesn't yet work
            fixed_input_symmetry_list = str(input_symmetry_list[i]).replace("(0,0)+(1/2, 1/2)", "")
            #plot_heatmap(fixed_input_symmetry_list)

if __name__ == "__main__":    
    input_symmetry = ["1a", "2e", "3c", "3ba", "4a", "5b", "6i", "6hg", "6he", "6hf", "6gf", "6ge", "6fe", "7d", "7cb", "8c", "9f", "9ed", "10d",
                      "11g", "11fe", "11fd", "11ed", "12d", "12cb", "13d", "14e", "14dc", "15d", "15cb", "16d", "17f", "17ed"]
    
    generate_heatmaps(input_symmetry)
