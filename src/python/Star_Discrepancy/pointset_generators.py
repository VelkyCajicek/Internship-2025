def generate_Bundschuh_Zhu_article_points(decimal_places : int = 7):
    # Resulting D* should be 0.849609
    points_x = [k/32 for k in range(0,32)]
    points_y = [round((7*k/32) % 1, decimal_places)  for k in range(0,32)]
    return [list(coordinate) for coordinate in zip(points_x, points_y)]

def generate_Eric_Thiemard_article_points():
    # Resulting D* should be 0.266667
    return [
        [0, 0], [0.5, 0.333333], [0.25, 0.666667], [0.75, 0.111111],
        [0.125, 0.444444], [0.625, 0.777778], [0.375, 0.222222], 
        [0.875, 0.555556], [0.0625, 0.888889], [0.5625, 0.037037]
    ]

def generate_halton_sequence_points(n : int = 10, dimensions : int = 2):
    
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
            
    match(dimensions):
        case 2: return [[x, y] for _, x, y in zip(range(n), halton_sequence(2), halton_sequence(3))]
        case 3: return [[x, y, z] for _, x, y, z in zip(range(n), halton_sequence(2), halton_sequence(3), halton_sequence(4))]
        case 4: return [[x, y, z, a] for _, x, y, z, a in zip(range(n), halton_sequence(2), halton_sequence(3), halton_sequence(4), halton_sequence(5))]
        
def generate_sobol_sequence_points(n : int = 10, dimensions : int = 2):
    # Sobol sequence imported from scipy
    from scipy.stats import _qmc
    # Algorithm generates point 2^m
    for power in range(n):
        if(2**power >= n):
            sampler = _qmc.Sobol(d=dimensions, scramble=False)
            sample = sampler.random_base2(m=power)
            
            return sample[:n]