import re
# For plotting
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
# For progress bar
import sys
import os
# Goes one directory down
sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
import Star_Discrepancy.QMC.Bundschuh_Zhu as BDZ

# TODO:
# Currently only works if there is an x and y

with open("Data\wyckoff_positions_2D_New.txt", "r") as data:
    lines = [line.strip() for line in data]

def obtain_user_input(user_input : str):    
    # This splits the code into individual chars
    input_info_list = list(user_input)
    # Range 3 since the multiplicity is at max a 3-digit number
    # Merges the multiplicity numbers into one int element 
    for i in range(0,3):
        try:
            if(not input_info_list[i].isdigit()): 
                input_info_list[0:i] = [int("".join(input_info_list[0:i]))]
        except(IndexError):
            break
    return input_info_list

def obtain_axis_data(input_info_list : list): 
    axis_strings = []
    multiplicities = []
    # Spaghetti code here, could do with some fixing 
    for i in range(len(lines)):
        # Yes, fr is actual syntax
        # Checks for line with # and number
        if(bool(re.match(fr"#\s{input_info_list[0]}$", lines[i]))):
            # Checks for following lines
            for j in range(1, len(lines)):
                if(len(axis_strings) == len(input_info_list) - 1):
                    break
                # Checks whether it hasnt gone outside of its given sequence
                elif(lines[i+j][0] == "#"):
                    print("Not valid sequence")
                    sys.exit()
                # Goes through the letters to check whether it isnt there 
                for k in range(1, len(input_info_list)):
                    if(input_info_list[k] in lines[i+j]):
                        axis_strings.append(lines[i+j])
                        # May not work for high multiplicities
                        multiplicities.append(int(lines[i+j][0:2]))

    return axis_strings, multiplicities

def split_string(axis_string):
    # Written originally by ChatGPT
    parts = [] 
    start = 0  
    comma_count = 0 

    for i, char in enumerate(axis_string):
        if char == ',':
            comma_count += 1  
            if comma_count == 2:
                parts.append(axis_string[start:i])
                start = i + 1  
                comma_count = 0  
    parts.append(axis_string[start:])

    return parts

# Removes integer part of float
def modulo_shift(point : float) -> float:
    return round(point % 1, 4)

# Checks for duplicate
def point_duplicate(point_x_to_check : float, point_y_to_check : float, point_set_x : list, point_set_y : list) -> bool:
    for i in range(len(point_set_x)):
        if(point_x_to_check in point_set_x):
            if(point_set_y[i] == point_y_to_check):
                return False
    return True
# Creates points
def create_pointset(x_value : float, y_value : float, coordinates : list) -> list:
    x_points_list = y_points_list = []
    for i in range(len(coordinates)):
        x_y_split = str(coordinates[i]).split(",")
        x_point = eval(x_y_split[0].replace("x", str(modulo_shift(x_value))).replace("y", str(modulo_shift(y_value))))
        y_point = eval(x_y_split[1].replace("x", str(modulo_shift(x_value))).replace("y", str(modulo_shift(y_value))))
        # Doesnt appened to list if a point exists in that specific location
        if(point_duplicate(x_point, y_point, x_points_list, y_points_list)):
            x_points_list.append(x_point)
            y_points_list.append(y_point)

    combined_point_list = []
    for i in range(len(x_points_list)):
        combined_point_list.append([x_points_list[i], y_points_list[i]])
    return combined_point_list
        
def create_heatmap_data(interpolated_points : int, txt_file_bool : bool, heatmap_bool : bool, coordinates : list, user_input_list : list) -> None:
    # This is if its done in Python
    # Comment out if running on something else
    # Start
    x_points = []
    y_points = []
    discrepancies = []
    # End 
    run_value = 0
    if(txt_file_bool):
        # Open .txt file / create one
        open(f"{user_input_list[0]}.txt", "w")
    for x in range(1,interpolated_points):
        string_list = []
        for y in range(1,interpolated_points):  
            points = create_pointset(x/interpolated_points, y/interpolated_points, coordinates)
            discrepancy = BDZ.Bundschuh_Zhu_Algorithm_WH(points)
            string_list.append(f"{x/interpolated_points} {y/interpolated_points} {discrepancy}\n")
            # Progress bar
            run_value +=1
            updt(interpolated_points**2, run_value)
            # Once again the following are to be commented out if not running in Python
            # Start
            if(heatmap_bool):
                x_points.append(x/interpolated_points)
                y_points.append(y/interpolated_points)
                discrepancies.append(discrepancy)
        if(txt_file_bool):
            with open(f"{user_input_list[0]}.txt", "a") as file:
                for i in range(len(string_list)):
                    file.write(string_list[i])
    run_value += (interpolated_points**2 - run_value)
    updt(interpolated_points**2, run_value)
    
    return x_points, y_points, discrepancies

    
def updt(total, progress):
    """
    Displays or updates a console progress bar.

    Original source: https://stackoverflow.com/a/15860757/1391441
    """
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

def plot_heatmap(x_points : list, y_points : list, values : list, multiplicities : list, user_input_list : list):
    # Written originally by ChatGPT
    # Define a finer grid for interpolation
    x_fine = np.linspace(min(x_points), max(x_points), 500)
    y_fine = np.linspace(min(y_points), max(y_points), 500)
    x_fine_grid, y_fine_grid = np.meshgrid(x_fine, y_fine)

    # Interpolate the values onto the finer grid
    points = np.column_stack((x_points, y_points))
    values_interpolated = griddata(points, values, (x_fine_grid, y_fine_grid), method='linear')

    # Plot the blend map
    plt.figure(figsize=(6, 5))
    plt.imshow(values_interpolated, extent=(min(x_points), max(x_points), min(y_points), max(y_points)), 
               origin='lower', cmap='seismic', aspect='auto')
    plt.colorbar(label='D*')
    try:
        plt.xlabel(f"{user_input_list[0]}{user_input_list[1]}")
        plt.ylabel(f"{user_input_list[0]}{user_input_list[2]}")
    except(IndexError):
        plt.xlabel("X")
        plt.ylabel("Y")
    concatenated_user_input_list = " ".join([str(value) for value in user_input_list])
    plt.title(f"{concatenated_user_input_list} (N = {sum(multiplicities)}, A = 2)")
    plt.show()

if __name__ == "__main__":
    # Main parameters
    wyckoff_symmetry = "17f"
    x_points_total = []
    y_points_total = []
    discrepancies_total = []
    # Parameters for create_heatmap_data function
    generate_txt_file = False
    generate_heatmap = True
    interpolations = 100
    # Run main
    user_input_list = obtain_user_input(wyckoff_symmetry)
    axis_strings, multiplicities = obtain_axis_data(user_input_list)
    
    for i in range(len(axis_strings)):
        # Spread on to 3 lines for readability
        axis_strings[i] = "".join(re.findall(r"\(.*,.*\)", axis_strings[i]))
        axis_strings[i] = axis_strings[i].replace("(", "").replace(")", "").replace("'", "").strip()
        axis_strings[i] = split_string(axis_strings[i])
    
    print("D* calculated, Creating heatmap")

    # May need to be taken out
    #axis_strings = list(itertools.chain(axis_strings))    
    x_points, y_points, discrepancies = create_heatmap_data(interpolations, generate_txt_file, generate_heatmap, axis_strings[0], user_input_list)

    plot_heatmap(x_points, y_points, discrepancies, multiplicities, user_input_list)