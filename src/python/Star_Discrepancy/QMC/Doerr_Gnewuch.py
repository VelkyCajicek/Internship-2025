def Gwenuch_Doerr_Algorithm(pointset : list[list]):
    n = len(pointset)  # Number of points
    d = len(pointset[0])  # Dimension
    max_discrepancy = 0
    
    for j in range(n):
        volume = 1
        for index in range(d):
            volume *= pointset[j][index]
        sigma = 0
        
        discrepancy = abs(volume - 1/n * 1)