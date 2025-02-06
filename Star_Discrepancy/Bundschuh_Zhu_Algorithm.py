import itertools

def create_test_case(format_value : int):
    points_x = [k/32 for k in range(0,32)]
    points_y = [round((7*k/32) % 1, 8) for k in range(0,32)]
    # Formats of test case
    # 1. Simply returns points_x and points_y 
    # 2. Returns a combined list ([x1, y1, ... ,xn, yn])
    # 3. Returns a list with coordinate formated values ([[x1,y1], ... , [xn, yn]])
    match(format_value):
        case 1: return points_x, points_y
        case 2: return list(itertools.chain.from_iterable(zip(points_x,points_y)))
        #case 3: return [

#def Bundschuh_Zhu_Algorithm_Wolfgang():
    

def Bundschuh_Zhu_Algorithm_lists(points_x, points_y):
    n = len(points_x)
    points_y_sorted = [x for _,x in sorted(zip(points_x,points_y))]
    points_x = [0.0] + points_x + [1.0]
    
    l_list = []
    for l in range(0,n+1):
        k_list = []
        # For now testing this
        try:
            xi_matrix = sorted(list(points_y_sorted[0:l])) + [1.0] # [0.0] + 
        except(TypeError):
            xi_matrix = [0.0, 1.0]
        # Algorithm itself
        for k in range(0,l+1):
            k_list.append(max(abs(k/n - points_x[l]*xi_matrix[k]), abs(k/n - points_x[l+1]*xi_matrix[k+1])))
        l_list.append(max(k_list))
    
    return max(k_list)

if __name__ == "__main__":
    points_x, points_y = create_test_case(1)
    #print(Bundschuh_Zhu_Algorithm_lists(points_x, points_y))
    result = [[x,y] for x,y in list(itertools.chain.from_iterable(zip(points_x,points_y)))]
    print(result)
    