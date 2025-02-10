import re
import sys

with open("Data\wyckoff_positions_2D_Letters.txt", "r") as data:
    lines = [line.strip() for line in data]

sequential_number_multiplicities = "17f"

# Will now use .txt file with wyckoff letters first
def check_validity_of_input(input : str):
    multiplicity_strings = []
    # Filter removes "" from list
    split_input = list(filter(None, re.split('(\d+)',input)))
    split_input[1] = list(split_input[1])
    for i in range(len(lines)):
        if(lines[i][1:4] == f"# {split_input[0]}"):
            for j in range(i, len(lines)):
                if(lines[i+j][0] == "#"):
                    break
                if(lines[i+j][0] in split_input):
                    multiplicity_strings.append(lines[j])
    print(multiplicity_strings)

check_validity_of_input(sequential_number_multiplicities)