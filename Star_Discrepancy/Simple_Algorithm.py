def create_test_case():
    points_x = [k/32 for k in range(0,32)]
    points_y = [7*k/32 for k in range(0,32)]
    # Point Shift
    for i in range(len(points_x)):
        points_x[i] = round(points_x[i] % 1, 8)
        points_y[i] = round(points_y[i] % 1, 8)
    return points_x, points_y

