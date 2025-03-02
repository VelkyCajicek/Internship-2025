import math

def hexagonal_transformation(pointset : list[list[float]]):
    # x_cartesian = x_hexagonal
    # -1/2x_cartesian + sqrt(3)/2*y_cartesian = y_hexagonal
    pass

def universal_transformation(pointset : list[list[float]], phi : float, a : float = 1) -> list[list[float]]:
    # u = y
    # v = x * tg(phi)
    transformed_pointset = []
    for i in range(len(pointset)):
        x = pointset[i][0]
        y = pointset[i][1]
        new_coordinate = [x * math.tan(phi), y]
        transformed_pointset.append(new_coordinate)
    return transformed_pointset
