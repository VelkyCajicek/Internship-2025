import sys
import os
import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
from Star_Discrepancy.QMC.Bundschuh_Zhu import Bundschuh_Zhu_Algorithm
from Diaphony.diaphony import Zinterhof_Diaphony
from Rhombus_Unit_Cell.shift_coordinates import hexagonal_transformation

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

def calculate_discrepancies(all_points : list, symmetry_name : str, interpolations : int, diaphony : bool, hexagonal_test : bool) -> list[float]:
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
    
    for x in range(0, interpolations):
        for y in range(0, interpolations):
            poinset = generate_pointset(round((x + center_value) / interpolations, 7), round((y + center_value) / interpolations, 7), all_points)
            #poinset = remove_duplicates(poinset)
            
            if(hexagonal_test):
                poinset = hexagonal_transformation(poinset)
                
            if(diaphony):
                discrepancies.append(Zinterhof_Diaphony(poinset))
            else:
                discrepancies.append(Bundschuh_Zhu_Algorithm(poinset))

            run_value += 1
            updt(interpolations**2, run_value)
    
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

def plot_heatmaps(symmetry_names : list[str], resolution : int = 100, diaphony : bool = False, create_pdf_files : bool = False, hexagonal_test : bool = False):
    pdf_file_name = "heatmaps_duplicates.pdf"
    if(hexagonal_test):
        pdf_file_name = "heatmaps_hex.pdf"
        # 13 - 17 for hexagonal test
        symmetry_names = ["13d", "14e", "15d", "16d", "17f", "17ed"]
    if(create_pdf_files):
        with PdfPages(pdf_file_name) as pdf:
            for symmetry_name in symmetry_names:
                # Moved here to count multiplicity
                all_points = []
                
                fig, ax = plt.subplots(figsize=(6, 6))  # Square figure to maintain aspect ratio
                discrepancies = calculate_discrepancies(all_points, symmetry_name, resolution, diaphony, hexagonal_test)
                heatmap_data = np.array(discrepancies).reshape(resolution, resolution)

                im = ax.imshow(heatmap_data, cmap='seismic', extent=[0, 1, 0, 1], origin='lower', interpolation='gaussian') # interpolation='gaussian' ensures smooth edges
                
                ax.set_title(f"{symmetry_name}, N = {len(all_points)}")
                ax.set_xlabel('X')
                ax.set_ylabel('Y')
                ax.set_aspect('equal')  # Ensures heatmap remains a square
                
                fig.colorbar(im, ax=ax, label=f"D* (Min: {min(discrepancies)}, Max: {max(discrepancies)})")
                
                pdf.savefig(fig)
                plt.close(fig)
                
        print(f"Saved all heatmaps to PDF")
    
    else:
        # If not saving to PDF, display plots individually
        for symmetry_name in symmetry_names:
            all_points = []
            
            fig, ax = plt.subplots(figsize=(6, 6))
            discrepancies = calculate_discrepancies(all_points, symmetry_name, resolution, diaphony, hexagonal_test)
            print("D* calculation finished; Creating heatmap ...")
            
            heatmap_data = np.array(discrepancies).reshape(resolution, resolution)

            im = ax.imshow(heatmap_data, cmap='seismic', extent=[0, 1, 0, 1], origin='lower', interpolation='gaussian') 

            ax.set_title(symmetry_name)
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_aspect('equal')
            fig.colorbar(im, ax=ax, label=f"D* (Min: {min(discrepancies)}, Max: {max(discrepancies)})")

            plt.show()
            plt.close(fig)

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
    
    plot_heatmaps(["17f"], create_pdf_files=True, hexagonal_test=False)