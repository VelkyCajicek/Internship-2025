import itertools
import bisect

def create_test_case(format_value : int):
    points_x = [k/32 for k in range(0,32)]
    points_y = [round((7*k/32) % 1, 4)  for k in range(0,32)]
    # Point Shift
    # Added options so the input could be altered
    match(format_value):
        # 1. Two seperate lists 
        case 1: return points_x, points_y
        # 2. One list with alternating values
        case 2: return list(itertools.chain.from_iterable(zip(points_x,points_y)))
        # 3. One list with coordinate style values (currently with lists) 
        case 3: return [list(coordinate) for coordinate in zip(points_x, points_y)]

def Bundschuh_Zhu_Algorithm_WH(pointset : list) -> float:
    n = len(pointset)
    # Sorts pointset based on x values
    sorted_pointset = sorted(pointset, key=lambda coord : coord[0])
    # Extracts x and y values
    x_values = [0.0] + [entry[0] for entry in sorted_pointset] + [1.0]
    y_values = [entry[1] for entry in sorted_pointset]
    # Creates y value matrix
    matrix_y = [[0.0] + sorted(y_values[0 : l]) + [1.0] for l in range(0, n+1)]
    # Discrepancy calculation
    max_discrepancy = 0.0
    for l in range(0, n+1):
        for k in range(0, l+1):
            # Calculation from the formula
            point_ratio = k / n
            area_one = x_values[l] * matrix_y[l][k]
            area_two = x_values[l+1] * matrix_y[l][k+1]
            discrepancy = max(point_ratio - area_one, area_two - point_ratio)
            # If discrepancy is larger append it
            if(discrepancy > max_discrepancy):
                max_discrepancy = discrepancy
    return round(max_discrepancy, 8)

# My attempt at optimalizing this
def Bundschuh_Zhu_Algorithm_TP(pointset : list) -> float:
    n = len(pointset)
    # Still unsure how necessary this is 
    # Sorts pointset based on x values
    sorted_pointset = sorted(pointset, key=lambda coord : coord[0])
    # Extracts x and y values
    x_values = [0.0] + [entry[0] for entry in sorted_pointset] + [1.0]
    y_values = [entry[1] for entry in sorted_pointset]
    max_discrepancy = 0
    for l in range(0, n+1):
        # Moved this calculation inside of calculation since it may be better for other programming languages
        matrix_y = [0.0] + sorted(y_values[0 : l]) + [1.0]
        for k in range(0, l+1):
            # Calculation from the formula
            point_ratio = k / n
            area_one = x_values[l] * matrix_y[k]
            area_two = x_values[l+1] * matrix_y[k+1]
            discrepancy = max(point_ratio - area_one, area_two - point_ratio)
            # If discrepancy is larger append it
            if(discrepancy > max_discrepancy):
                max_discrepancy = discrepancy
    return round(max_discrepancy, 8)

def Bundschuh_Zhu_Algorithm_TP2(pointset : list) -> float:
    n = len(pointset)
    # Sorts pointset based on x values
    sorted_pointset = sorted(pointset, key=lambda coord : coord[0])
    # Extracts x and y values
    x_values = [0.0] + [entry[0] for entry in sorted_pointset] + [1.0]
    y_values = [entry[1] for entry in sorted_pointset]
    y_matrix_values = []
    max_discrepancy = 0
    for l in range(0, n+1):
        # Using a if statement and doing it by inserting a value is still faster than re-sorting
        if l > 0: bisect.insort(y_matrix_values, y_values[l-1])
        matrix_y = [0.0] + y_matrix_values + [1.0]
        for k in range(0, l+1):
            # Calculation from the formula
            point_ratio = k / n
            area_one = x_values[l] * matrix_y[k]
            area_two = x_values[l+1] * matrix_y[k+1]
            discrepancy = max(point_ratio - area_one, area_two - point_ratio)
            # If discrepancy is larger append it
            if(discrepancy > max_discrepancy):
                max_discrepancy = discrepancy
    return round(max_discrepancy, 8)

if __name__ == "__main__":
    # SUMMARY
    # Times are virtually the same and these values depend quite significantly on what order the functions are run
    # TP : Put the matrice calculation into the l for loop so theoretically it could be slightly better,
    #      since its one for loop less and its no longer a 2D array
    # TP2 : Instead of sorting the entire list at each index in the y matrice,
    #       it inserts the next y value into to correct position inside of the array
    # All of these return the same correct values
    print(Bundschuh_Zhu_Algorithm_WH(create_test_case(3)))
    print(Bundschuh_Zhu_Algorithm_TP(create_test_case(3)))
    print(Bundschuh_Zhu_Algorithm_TP2(create_test_case(3)))