import os
import matplotlib.pyplot as plt
import numpy as np
import re

# Changes path of working directory
path = os.path.realpath(__file__)
dir = os.path.dirname(path)
dir = dir.replace("Transformations", "Data")
os.chdir(dir)

with open("wyckoff_positions_2D_New.txt", "r") as data:
    lines = [line.strip() for line in data]

def obtain_user_input(user_input : str):    
    # This splits the code into individual chars
    input_info_list = list(user_input)

    # Range 3 since the multiplicity is at max a 3-digit number
    # Merges the multiplicity numbers into one int element 
    for i in range(0,3):
        if(not input_info_list[i].isdigit()): 
            input_info_list[0:i] = [int("".join(input_info_list[0:i]))]
    
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
                    break
                # Goes through the letters to check whether it isnt there 
                for k in range(1, len(input_info_list)):
                    if(input_info_list[k] in lines[i+j]):
                        axis_strings.append(lines[i+j])
                        # May not work for high multiplicities
                        multiplicities.append(int(lines[i+j][0:2]))

    return axis_strings, multiplicities

def generate_points(points_x : list, points_y : list, axis_string : str):
    # Find the max and minumum values
    min_x = min_y = max_x = max_y = 0
    coordinates = re.findall(r"\(.*,.*\)", axis_string)[0].split("',")
    # Values to transform plane
    for i in range(len(coordinates)):
        # Also should be improved, removes shit
        coordinates[i] = (str(coordinates[i]).replace("'", "").replace("(", "").replace(")", "")
                          # These two lines to ensure the other options
                          #.replace("2", "2*")
                          #.replace("3", "3*")
                          .strip())
        # Finds maximums and minima
        # Also not too proud of this
        temp_coords = coordinates[i].split(",")
        if(min_x > eval(temp_coords[0].replace("x", "1"))):
            min_x = eval(temp_coords[0].replace("x", "1"))
        if(max_x < eval(temp_coords[0].replace("x", "1"))):
            max_x = eval(temp_coords[0].replace("x", "1"))
        if(min_y > eval(temp_coords[1].replace("x", "1"))):
            min_y = eval(temp_coords[1].replace("x", "1"))
        if(max_y < eval(temp_coords[1].replace("x", "1"))):
            max_y = eval(temp_coords[1].replace("x", "1"))

    # Plot points        
    for i in range(len(coordinates)):
        temp_coords = coordinates[i].split(",")
        for value in range(0, 100):
            points_x.append(coordinate_shift(min_x, min_y, max_x, max_y, eval(temp_coords[0].replace("x", str(value / 100)))))
            points_y.append(coordinate_shift(min_x, min_y, max_x, max_y, None, eval(temp_coords[1].replace("x", str(value / 100)))))

def coordinate_shift(min_x, min_y, max_x, max_y, x = None, y = None):
    if(x != None): return float((x - min_x) / (max_x - min_x))
    else: return float((y - min_y) / (max_y - min_y))

if __name__ == "__main__":
    points_x = []
    points_y = []
    multiplicities = []
    
    test_input = "11efa"
    user_input_list = obtain_user_input(test_input)
    axis_strings, multiplicities = obtain_axis_data(user_input_list)
    concatenated_user_input_list = " ".join([str(value) for value in user_input_list])
    
    for i in range(len(axis_strings)):
        generate_points(points_x, points_y, axis_strings[i])
    
    x_axis = np.array(points_x)
    y_axis = np.array(points_y)

    plt.scatter(x_axis,y_axis)
    plt.title(f"{concatenated_user_input_list} (N = {sum(multiplicities)}, A = 2)")
    plt.xlabel(f"{user_input_list[0]}{user_input_list[1]}")
    plt.ylabel(f"{user_input_list[0]}{user_input_list[2]}")
    plt.show()    
