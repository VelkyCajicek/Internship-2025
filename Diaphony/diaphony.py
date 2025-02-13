import math

def create_halton_sequence_points(n : int = 10, dimensions : int = 2):

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

def create_sobol_sequence_points(n : int = 10, dimensions : int = 2):
    # Sobol sequence imported from scipy
    from scipy.stats import _qmc
    # Algorithm generates point 2^m
    for power in range(n):
        if(2**power >= n):
            sampler = _qmc.Sobol(d=dimensions, scramble=False)
            sample = sampler.random_base2(m=power)

            return sample[:n]

def e_h(x : int):
    return math.exp(2*math.pi*1j)
    
def S_N(pointset):
    N = len(pointset)
    return 1/N * sum([])

if __name__ == "__main__":
    print(create_sobol_sequence_points(n=12))