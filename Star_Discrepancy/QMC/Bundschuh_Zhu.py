import bisect

def Bundschuh_Zhu_Algorithm(pointset : list[list]) -> float:
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
 