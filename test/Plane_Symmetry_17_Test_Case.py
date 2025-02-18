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

coordinates = ['x,y', '-y,x-y', '-x+y,-x', '-x,-y', 'y,-x+y', 'x-y,x', '-y,-x', '-x+y,y', 'x,x-y', 'y,x', 'x-y,-y', '-x,-x+y']

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
        
def create_heatmap_data(interpolated_points : int, txt_file_bool : bool, heatmap_bool : bool) -> None:
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
        open("17.txt", "w")
    for x in range(1,interpolated_points):
        string_list = []
        for y in range(1,interpolated_points):  
            points = create_pointset(x/interpolated_points,y/interpolated_points,coordinates)
            discrepancy = BDZ.Bundschuh_Zhu_ChatGPT(points, (x/interpolated_points, y/interpolated_points))
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
            with open("17.txt", "a") as file:
                for i in range(len(string_list)):
                    file.write(string_list[i])
    run_value += (interpolated_points**2 - run_value)
    updt(interpolated_points**2, run_value)
    print("Discrepancy calculated, Creating heatmap")
    # Also commented out after
    # Start
    plot_heatmap(x_points, y_points, discrepancies)
    # End
    
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

def plot_heatmap(x_points : list, y_points : list, values : list):
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
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('17')
    plt.show()

if __name__ == "__main__":
    # Main parameters
    generate_txt_file = False
    generate_heatmap = True
    interpolations = 100
    # Run main
    create_heatmap_data(interpolations, generate_txt_file, generate_heatmap)