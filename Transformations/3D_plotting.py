import re
import numpy as np
import matplotlib.pyplot as plt

# Notes to self:
# May need to set z values to 0 for now to at least tell whether I am doing this correctly


y_axis_raw = "12 : h : ['(x,1/2,0)', '(-x,1/2,0)', '(0,x,1/2)', '(0,-x,1/2)', '(1/2,0,x)', '(1/2,0,-x)', '(1/2,x,0)', '(1/2,-x,0)', '(x,0,1/2)', '(-x,0,1/2)', '(0,1/2,-x)', '(0,1/2,x)'] "
x_axis_raw = "6 : e : ['(x,0,0)', '(-x,0,0)', '(0,x,0)', '(0,-x,0)', '(0,0,x)', '(0,0,-x)'] "

def extract_bracket_values_xy(input_string):
    extracted_values = re.findall(r"\((.*?)\)", input_string)
    x_values = []
    y_values = []
    z_values = []
    for value in extracted_values:
        x, y, z = value.split(',')
        x_values.append(x.strip())
        y_values.append(y.strip())
        z_values.append(z.strip())

    return x_values, y_values, z_values

x_axis, y_axis, z_axis = extract_bracket_values_xy(x_axis_raw)

print(x_axis)
print(y_axis)
print(z_axis)

fitted_coordinates_x = []
fitted_coordinates_y = []
# X axis
for i in range(len(x_axis)):
    # Goes through coordinates
    for j in range(0, 100, 1):
        try:
            fitted_coordinates_x.append(float(x_axis[i]) / 100)
        except(ValueError):
            fitted_coordinates_x.append(i)
# Y axis
for i in range(len(y_axis)):
    # Goes through coordinates
    for j in range(0, 100, 1):
        try:
            fitted_coordinates_y.append(float(y_axis[i]) / 100)
        except(ValueError):
            fitted_coordinates_y.append(i)    

print(len(fitted_coordinates_x))

x = np.array(fitted_coordinates_x)
y = np.array(fitted_coordinates_y)

plt.scatter(x,y)
plt.show()