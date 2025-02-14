from performance_testing import test_discrepancies, time_functions

if __name__ == "__main__":
    star_discrepancy_algorithms = ["Bundschuh_Zhu_Algorithm", "simple_D_star"]
    
    test_discrepancies(star_discrepancy_algorithms)
    
    #time_functions(star_discrepancy_algorithms)