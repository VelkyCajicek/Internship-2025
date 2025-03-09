import sys
import os
import re
import numpy as np
import matplotlib.pyplot as plt

sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
from Star_Discrepancy.QMC.Bundschuh_Zhu import Bundschuh_Zhu_Algorithm

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
        coordinates[0] = round(eval(str(coordinates[0]).replace('x', str(x_value)).replace('y', str(y_value))) % 1, 7)
        coordinates[1] = round(eval(str(coordinates[1]).replace('x', str(x_value)).replace('y', str(y_value))) % 1, 7)
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

def get_specific_pointset(symmetry_name : str, remove_duplicates_var : bool, x : float = 0, y : float = 0, decimal_points : int = 7):
    center_value = 0
    
    # For symmetries 5 and 9
    if(symmetry_name[0] == "5" or symmetry_name[0] == "9"):
        center_value = 0.5
    
    point_formulas = get_point_formulas(symmetry_name)
    point_formulas = add_degree_of_freedom(point_formulas)
    individual_formulas = [extract_parentheses(point_formulas[i]) for i in range(len(point_formulas))]
    
    all_points = []
    [all_points.extend(element) for element in individual_formulas]

    pointset = generate_pointset(round((x + center_value), decimal_points), round((y + center_value), decimal_points), all_points)
    
    if(remove_duplicates_var):
        pointset = remove_duplicates(pointset)
    
    return pointset

def get_specific_discrepancy(pointset):
    return Bundschuh_Zhu_Algorithm(pointset)

def calculate_discrepancies(symmetry_name : str, resolution : int, remove_duplicates_var : bool, decimal_places : int) -> list[float]:
    all_points = []
    discrepancies = []
    run_value = 0
    center_value = 0
    
    # For symmetries 5 and 9
    if(symmetry_name[0] == "5" or symmetry_name[0] == "9"):
        center_value = 0.5
    
    point_formulas = get_point_formulas(symmetry_name)
    point_formulas = add_degree_of_freedom(point_formulas)
    
    individual_formulas = [extract_parentheses(point_formulas[i]) for i in range(len(point_formulas))]
    
    [all_points.extend(element) for element in individual_formulas]
    
    # Calculates the D*
    
    for x in range(0, resolution):
        for y in range(0, resolution):
            poinset = generate_pointset(round((x + center_value) / resolution, decimal_places), round((y + center_value) / resolution, decimal_places), all_points)
            
            if(remove_duplicates_var):
                poinset = remove_duplicates(poinset)
            
            discrepancies.append(Bundschuh_Zhu_Algorithm(poinset))

            run_value += 1
            updt(resolution**2, run_value)
    
    return discrepancies

def add_degree_of_freedom(point_list : list[str]) -> list[str]:
    if(len(point_list) == 1):
        return point_list
    
    if("x" in point_list[0] and "y" not in point_list[1]):
        point_list[1] = point_list[1].replace("x", "y")
        return point_list
    
    if("y" in point_list[0] and "x" not in point_list[1]):
        point_list[1] = point_list[1].replace("x", "y")
        return point_list
    
    return point_list

def plot_heatmaps(symmetry_name : str, selected_interpolation : str = "gaussian", selected_cmap : str = "seismic", resolution : int = 100, remove_duplicates : bool = False, decimal_places : int = 7):
    fig, ax = plt.subplots(figsize=(6, 6))
    discrepancies = calculate_discrepancies(symmetry_name, resolution, remove_duplicates, decimal_places)
    print("D* calculation finished; Creating heatmap ...")
            
    heatmap_data = np.array(discrepancies).reshape(resolution, resolution)

    im = ax.imshow(heatmap_data, cmap=selected_cmap, extent=[0, 1, 0, 1], origin='lower', interpolation=selected_interpolation) 

    # May be ineffective, but removes the need for all points to be imported and causing a mess
    ax.set_title(f"{symmetry_name}, N = {len(get_specific_pointset(symmetry_name, remove_duplicates_var=False))}")
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_aspect('equal')
    fig.colorbar(im, ax=ax, label=f"D* (Min: {min(discrepancies)}, Max: {max(discrepancies)})")

    return fig

def updt(total, progress) -> None:
    barLength, status = 20, ""
    progress = float(progress) / float(total)
    if progress >= 1.:
        progress, status = 1, "\r\n"
    block = int(round(barLength * progress))
    text = "\r[{}] {:.0f}% {}".format(
        "#" * block + "-" * (barLength - block), round(progress * 100, 0), status)
    sys.stdout.write(text)
    sys.stdout.flush()

if __name__ == "__main__":
    # All with 2 degrees of freedom  
    input_symmetry = ["1a", "2e", "3c", "4a", "5b", "6i", "6he", "6hf", "6gf", "6ge", "6fe", "7d", "8c", "9f", "9ed", "10d",
                      "11g", "11fe", "11fd", "11ed", "12d", "13d", "14e", "15d", "16d", "17f", "17ed"]
    
    plot_heatmaps(["17f"])