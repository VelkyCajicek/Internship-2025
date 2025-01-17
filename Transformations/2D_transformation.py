import os
import re
# Changes path of working directory
path = os.path.realpath(__file__)
dir = os.path.dirname(path)
dir = dir.replace("Transformations", "Data")
os.chdir(dir)

with open("wyckoff_positions_2D_Final.txt", "r") as data:
    lines = [line.strip() for line in data]
    
def get_current_symmetry(desired_index):
    for i in range(len(lines)):
        if bool((re.match(f"#\s{desired_index}", f"# {desired_index}"))):
            for j in range(i + 1, len(lines)):
                if(lines[i+j][0] == "#"):
                    return lines[i + 1: i+j]
                
print(get_current_symmetry(4))

print(bool((re.match("#\s[0-9]+", f"# {4}"))))