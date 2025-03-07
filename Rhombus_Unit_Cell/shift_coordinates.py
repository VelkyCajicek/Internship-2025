import math

def universal_transformation(pointset : list[list[float]], phi : float, a : float = 1) -> list[list[float]]:
    # x' = x/a - (y*cot(phi))/a
    # y' = y/a*sin(phi)
    transformed_pointset = []
    for i in range(len(pointset)):
        x = pointset[i][0]
        y = pointset[i][1]
        new_coordinate = [x / a - (y * 1/math.tan(phi)) / a, y/a*math.sin(phi)]
        transformed_pointset.append(new_coordinate)
    
    return transformed_pointset

if __name__ == "__main__":
    pointset = [
        [0,0], [1,0], [0.5,0.5]
    ]
    new_pointset = universal_transformation(pointset, 45, 1)
    print(new_pointset)