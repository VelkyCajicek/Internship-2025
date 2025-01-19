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
            # Rounding may be a mistake
            x_point = round(eval(temp_coords[0].replace("x", str(value / 100))), 2)
            y_point = round(eval(temp_coords[1].replace("x", str(value / 100))), 2)
            
            #points_x.append(coordinate_shift(min_x, min_y, max_x, max_y, x_point))
            #points_y.append(coordinate_shift(min_x, min_y, max_x, max_y, None, y_point))            
            
            # Assuming there cant be more than 1 point in one spot
            if(check_for_point(points_x, points_y, x_point, y_point)): 
                # Assuming multiple points go in the same spot
                points_x.append(coordinate_shift(min_x, min_y, max_x, max_y, x_point))
                points_y.append(coordinate_shift(min_x, min_y, max_x, max_y, None, y_point))
            else:
                continue

def check_for_point(points_x : list, points_y : list, x_point : float, y_point : float):
    for i in range(len(points_x)):
        if(points_x[i] == x_point):
            if(points_y[i] == y_point):
                return False
    return True

def coordinate_shift(min_x, min_y, max_x, max_y, x = None, y = None):
    # Try must be here if there is no coordinate shift and you have the point [0,0]
    # This is all assuming points with a different letter arent moved
    try:
        if(x != None): return float((x - min_x) / (max_x - min_x))
        else: return float((y - min_y) / (max_y - min_y))
    except(ZeroDivisionError):
        return float(0)

def local_star_discrepancy():
    pass

if __name__ == "__main__":
    points_x = []
    points_y = []
    multiplicities = []
    heatmap_bool = True
    # User input here for now
    test_input = "11fea"
    
    user_input_list = obtain_user_input(test_input)
    axis_strings, multiplicities = obtain_axis_data(user_input_list)
    # Must do this since fstrings hate "".join() for some reason
    concatenated_user_input_list = " ".join([str(value) for value in user_input_list])
    
    for i in range(len(axis_strings)):
        generate_points(points_x, points_y, axis_strings[i])
    # Convert lists to numpy arrays for graphing
    x_axis = np.array(points_x)
    y_axis = np.array(points_y)

    if(heatmap_bool):
        # Heatmap
        heatmap, xedges, yedges = np.histogram2d(x_axis, y_axis, bins=50)
        extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
        plt.clf()
        # Good cmaps: seismic, PiYG 
        plt.imshow(heatmap.T, extent=extent, origin='lower', interpolation='bilinear', cmap="seismic")
        plt.title(f"{concatenated_user_input_list} (N = {sum(multiplicities)}, A = 2)")
        plt.xlabel(f"{user_input_list[0]}{user_input_list[1]}")
        plt.ylabel(f"{user_input_list[0]}{user_input_list[2]}")
    else:
        # Scatter plot
        plt.scatter(x_axis,y_axis)
        plt.title(f"{concatenated_user_input_list} (N = {sum(multiplicities)}, A = 2)")
        plt.xlabel(f"{user_input_list[0]}{user_input_list[1]}")
        plt.ylabel(f"{user_input_list[0]}{user_input_list[2]}")

    plt.show()    
