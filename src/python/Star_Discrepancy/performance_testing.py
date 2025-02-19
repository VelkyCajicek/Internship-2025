import timeit
from python.Transformations.Bundschuh_Zhu import Bundschuh_Zhu_Algorithm, Tovstik_Improvement
from QMC.Doerr_Gnewuch import Gwenuch_Doerr_Algorithm
from Simple_Algorithm import Simple_D_star
from pointset_generators import generate_Bundschuh_Zhu_article_points, generate_Eric_Thiemard_article_points, generate_halton_sequence_points, generate_sobol_sequence_points

def time_functions(function_list : list[str], function_iterations : int = 100) -> None:
    for i in range(len(function_list)):
        current_function_time = timeit.timeit(stmt=function_list[i], 
                                              number=function_iterations,
                                              globals=globals())
        print(f"{function_list[i]} : {current_function_time}")

def test_discrepancies(functions_to_test : list[str]):
    # For now these will be default
    test_pointsets = [generate_Bundschuh_Zhu_article_points(),
                      generate_Eric_Thiemard_article_points(), 
                      generate_halton_sequence_points(100), 
                      generate_halton_sequence_points(500), 
                      generate_halton_sequence_points(1000), 
                      generate_halton_sequence_points(2000)]
    
    pointset_names = ["Bundschuh Zhu paper (0.849609): ",
                      "Eric Thiemard test case (0.266667): ", 
                      "Halton sequence (N = 100) : ",
                      "Halton sequence (N = 500) : ",
                      "Halton sequence (N = 1000) : ",
                      "Halton sequence (N = 2000) : ",]
    
    for i in range(len(functions_to_test)):
        print(f"{functions_to_test[i]}")
        for j in range(len(test_pointsets)):
            pointset_names[j] = pointset_names[j].replace("(pointset)", "")
            print(f"{pointset_names[j]}{globals()[str(functions_to_test[i])](test_pointsets[j])}")
        print()