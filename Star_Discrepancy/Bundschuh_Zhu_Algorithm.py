import bisect
import timeit

def create_test_case_paper(decimal_places : int = 7):
    # Resulting D* should be 0.849609
    points_x = [k/32 for k in range(0,32)]
    points_y = [round((7*k/32) % 1, decimal_places)  for k in range(0,32)]
    return [list(coordinate) for coordinate in zip(points_x, points_y)]

def create_Eric_Thiemard_points():
    # Resulting D* should be 0.266667
    pointset = [
        [0,0],
        [0.5,0.333333] ,
        [0.25, 0.666667],
        [0.75, 0.111111],
        [0.125, 0.444444],
        [0.625, 0.777778],
        [0.375, 0.222222],
        [0.875, 0.555556],
        [0.0625, 0.888889],
        [0.5625, 0.037037]
    ]
    return pointset

def create_halton_sequence_points(n : int = 10):

    def halton_sequence(b):
        # Generator function for Halton sequence from wikipedia
        n, d = 0, 1
        while True:
            x = d - n
            if x == 1:
                n = 1
                d *= b
            else:
                y = d // b
                while x <= y:
                    y //= b
                n = (b + 1) * y - x
            yield n / d

    return [[x, y] for _, x, y in zip(range(n), halton_sequence(2), halton_sequence(3))]

def time_functions(function_list : list[str], function_iterations : int = 100) -> None:
    for i in range(len(function_list)):
        current_function_time = timeit.timeit(stmt=function_list[i], 
                                              number=function_iterations,
                                              globals=globals())
        print(f"{function_list[i].replace("(pointset)", "")} : {current_function_time}")

def test_discrepancies(functions_to_test : list[str]):
    # For now these will be default
    test_pointsets = [create_test_case_paper(),
                      create_Eric_Thiemard_points(), 
                      create_halton_sequence_points(100), 
                      create_halton_sequence_points(500), 
                      create_halton_sequence_points(1000), 
                      create_halton_sequence_points(2000)]
    
    pointset_names = ["Bundschuh Zhu paper (0.849609): ",
                      "Eric Thiemard test case (0.266667): ", 
                      "Halton sequence (N = 100) : ",
                      "Halton sequence (N = 500) : ",
                      "Halton sequence (N = 1000) : ",
                      "Halton sequence (N = 2000) : ",]
    
    for i in range(len(functions_to_test)):
        print(f"{functions_to_test[i]}")
        for j in range(len(test_pointsets)):
            print(f"{pointset_names[j]}{globals()[str(functions_to_test[i])](test_pointsets[j])}")
        print()

def Bundschuh_Zhu_Algorithm_WH(pointset : list[list]) -> float:
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
    return round(max_discrepancy, 7)

# My attempt at optimalizing this
def Bundschuh_Zhu_Algorithm_TP(pointset : list[list]) -> float:
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
    return round(max_discrepancy, 7)

def Bundschuh_Zhu_Algorithm_TP2(pointset : list[list]) -> float:
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
    return round(max_discrepancy, 7)

def Bundschuh_Zhu_Algorithm_Display_Coordinate(pointset : list[list]) -> None:
    n = len(pointset)
    # Sorts pointset based on x values
    sorted_pointset = sorted(pointset, key=lambda coord : coord[0])
    # Extracts x and y values
    x_values = [0.0] + [entry[0] for entry in sorted_pointset] + [1.0]
    y_values = [entry[1] for entry in sorted_pointset]
    y_matrix_values = []
    max_discrepancy = 0
    # Added for saving coordinate
    x_coordinate = 0.0
    y_coordinate = 0.0
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
                x_coordinate = x_values[l]
                y_coordinate = matrix_y[k]
    print(f"Star discrepancy is {round(max_discrepancy, 8)} and this was found at the point [{x_coordinate},{y_coordinate}]")

# Works
def Tovstik_Improvement(pointset : list[list]):
    N = len(pointset)
    
    sorted_pointset = sorted(pointset, key=lambda coord : coord[0])
    # Only seems to work without [0.0] and [1.0]
    x_values = [entry[0] for entry in sorted_pointset]
    y_values = [entry[1] for entry in sorted_pointset]
    
    # Adding max here also returns the incorrect value somehow
    d2 = 0
    
    for j in range(N):
        mu = 0  
        v = 0 
        for i in range(N):
            if y_values[i] <= y_values[j]:
                v += 1
                point_ratio = v / N
                area = x_values[i] * y_values[j]
                discrepancy_value = abs(point_ratio - area)
                d2 = max(d2, discrepancy_value)
                
                if mu > 1:
                    previous_point_ratio = (v - 1) / N
                    previous_discrepancy_value = abs(previous_point_ratio - area)
                    d2 = max(d2, previous_discrepancy_value)
            else:
                mu += 1  
    
    return round(d2, 7) 

# Doesnt work
def Tovstik_Improvement_2(pointset : list[list]):
    N = len(pointset)
    
    sorted_pointset = sorted(pointset, key=lambda coord : coord[0])
    # Only seems to work without [0.0] and [1.0]
    x_values = [entry[0] for entry in sorted_pointset]
    y_values = [entry[1] for entry in sorted_pointset]
    
    def s_function(i : int, j : int, v : int):
        return max(v/N - x_values[i]*y_values[j], x_values[i+1]*x_values[i+1] - v/N)
    
    # Adding max here also returns the incorrect value somehow
    d2 = 0
    
    for j in range(N-1):
        mu = 0  
        v = 0 
        for i in range(N-1):
            if y_values[i] <= y_values[j]:
                v += 1
                s1 = s_function(i, j, v)
                d2 = max(d2, s1)
                
                if mu > 1:
                    s2 = s_function(i, j, v-1)
                    d2 = max(d2, s2)
            else:
                mu += 1  
    
    return round(d2, 8) 
    
if __name__ == "__main__":
    # Integrate this into the time_functions
    pointset = create_Eric_Thiemard_points()
    
    # Time all variations of algorithm
    
    time_functions(["Tovstik_Improvement(pointset)",
                    "Bundschuh_Zhu_Algorithm_TP(pointset)", 
                    "Bundschuh_Zhu_Algorithm_TP2(pointset)", 
                    "Bundschuh_Zhu_Algorithm_WH(pointset)"])
    
    # Tests different functions against each other
    
    test_discrepancies(["Tovstik_Improvement",
                        "Bundschuh_Zhu_Algorithm_TP2"])
    
    
   