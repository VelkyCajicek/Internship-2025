from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

# Implemented the simplest version as is in github readme
def Simple_D_star(pointset : list[list], area : tuple = (1,1), interpolations : int = 1000):
    discrepancies = []
    area_x, area_y = area

    points_x = [entry[0] for entry in pointset]
    points_y = [entry[1] for entry in pointset]

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

    for x in range(0, area_x * interpolations):
        for y in range(0, area_y * interpolations):
            points_inside_area = find_points_inside_area(points_x, points_y, x/interpolations, y/interpolations)
            discrepancies.append(abs(points_inside_area/len(points_x) - x/interpolations*y/interpolations / area_x*area_y))
    
    return round(max(discrepancies), 7)
