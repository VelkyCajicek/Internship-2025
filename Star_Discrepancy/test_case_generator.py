import random

def show_pointset(pointset : list) -> None:
    for i in range(len(pointset)):
        print(f"{pointset[i]}")

def generate_pointset(n : int, repeating_probability : float = 0, decimal_places : int = 8) -> list:
    # Code in this is ugly as shit but it works
    # Repeating probability should be between 0 and 1
    points_x = []
    points_y = []
    for i in range(n):
        # Uniform instead of randint since it returns floats instead of ints
        x = round(random.uniform(0,1), decimal_places)
        y = round(random.uniform(0,1), decimal_places)
        # Chooses a random value between 1,100 (1% - 100%) and checks whether its larger than the probability * 100
        if(random.randint(1,100) <= int(repeating_probability*100) and i != 0):
            # True for x coordinate, False for y coordinate
            if(random.choice([True, False])):
                x = random.choice(points_x)
            else:
                y = random.choice(points_y)

        points_x.append(x)
        points_y.append(y)
    
    return sorted([list(coordinate) for coordinate in zip(points_x, points_y)], key=lambda coord : coord[0])

# Switches all duplicate x values
def create_permutation_list(pointset : list):
    pass

if __name__ == "__main__":
    pointset = generate_pointset(10, repeating_probability=0.3, decimal_places=1)
    show_pointset(pointset)