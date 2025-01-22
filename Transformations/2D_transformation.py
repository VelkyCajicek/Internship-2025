import os
import re
#import matplotlib.pyplot as plt
#import numpy as np
# Changes path of working directory
path = os.path.realpath(__file__)
dir = os.path.dirname(path)
dir = dir.replace("Transformations", "Data")
os.chdir(dir)

with open("wyckoff_positions_2D_Final.txt", "r") as data:
    lines = [line.strip() for line in data]
    
# Code in this function is shit (could likely do with some fixing)
def get_current_symmetry(desired_index : int): 
    start_index = 0
    for i in range(0, len(lines)):
        if bool((re.match(r"#\s" + str(desired_index), lines[i]))):
            start_index = i
            break
    if(desired_index == 17):
        return lines[start_index + 1:]
    else:
        for i in range(start_index + 1, len(lines)):
            if(lines[i][0] == "#"):
                return lines[start_index + 1: i]

def extract_bracket_values(input_string):
    extracted_values = re.findall(r"\((.*?)\)", input_string)
    x_values = []
    y_values = []
    for value in extracted_values:
        x, y = value.split(',')
        x_values.append(x.strip())
        y_values.append(y.strip())

    return x_values, y_values

# General formula (which is useless)
# x(new) = (x-x(min))/(x(max) - x(min))
# y(new) = (y-y(min))/(x(max) - x(min))

def main(desired_index : int):
    new_x_values = []
    new_y_values = []
    # Current symmetry variable is a list
    current_symmetry = get_current_symmetry(desired_index)
    for symmetry in current_symmetry:
        x_values, y_values = extract_bracket_values(symmetry)
        for i in range(len(x_values)):
            new_x_values.append(float((x_values[i] - min(x_values)) / (max(x_values) - min(x_values))))
            new_y_values.append(float((y_values[i] - min(y_values)) / (max(y_values) - min(y_values))))
    

if __name__ == "__main__":
    main(2)