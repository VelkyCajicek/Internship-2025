from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

def create_test_case():
    points_x = [k/32 for k in range(0,32)]
    points_y = [7*k/32 for k in range(0,32)]
    # Point Shift
    for i in range(len(points_x)):
        points_x[i] = round(points_x[i] % 1, 8)
        points_y[i] = round(points_y[i] % 1, 8)
    return points_x, points_y

# Points_or_x is 
def find_points_inside_area(points_x : list, points_y : list, x_area_coordinate : float, y_area_coordinate : float) -> int:
    points_shapely = []
    total_points = 0
    for i in range(len(points_x)):
        points_shapely.append(Point(points_x[i], points_y[i]))
    # (x,y,[z]) Creates area
    discrepancy_area = Polygon([(0,0), (0, y_area_coordinate), (x_area_coordinate, y_area_coordinate), (x_area_coordinate, 0), (0,0)])
    # Checks whether point is in area
    for i in range(len(points_shapely)):
        if(discrepancy_area.contains(points_shapely[i])):
            total_points += 1
    return total_points

# Implemented the simplest version as is in github readme
def simple_D_star(points_x : list, points_y : list, area : tuple = (1,1), interpolations : int = 100):
    discrepancies = []
    area_x, area_y = area
    for x in range(0, area_x * interpolations):
        for y in range(0, area_y * interpolations):
            points_inside_area = find_points_inside_area(points_x, points_y, x/interpolations, y/interpolations)
            discrepancies.append(abs(points_inside_area/len(points_x) - x/interpolations*y/interpolations / area_x*area_y))
    return max(discrepancies)

if __name__ == "__main__":
    points_x, points_y = create_test_case()
    max_discrepancy = simple_D_star(points_x, points_y)
    print(max_discrepancy)
