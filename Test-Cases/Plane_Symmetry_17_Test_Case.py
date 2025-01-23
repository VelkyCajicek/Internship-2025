import os
import re
''''''
path = os.path.realpath(__file__)
dir = os.path.dirname(path)
dir = dir.replace("Test-Cases", "Data")
os.chdir(dir)

with open("wyckoff_positions_2D_New.txt", "r") as data:
    lines = [line.strip() for line in data]

axis_string = "".join(re.findall(r"\(.*,.*\)", lines[83]))

def split_string(axis_string):
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

coordinates = split_string(axis_string)

for i in range(len(coordinates)):
    coordinates[i] = coordinates[i].replace("(", "").replace(")", "").replace("'", "").strip()

coordinates = ['x,y', '-y,x-y', '-x+y,-x', '-x,-y', 'y,-x+y', 'x-y,x', '-y,-x', '-x+y,y', 'x,x-y', 'y,x', 'x-y,-y', '-x,-x+y']

print(coordinates)