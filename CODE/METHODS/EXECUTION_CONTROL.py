from CODE.METHODS.FUNCTIONS import _GA, _SA
import time

def execute_function(method_id, function_object, args):
    print("New Function Execution")
    print(method_id)
    print(function_object)
    
    parameters = []

    x = time.time()
    if method_id == 1:
        # population_size, generation, elite_count, crossover_rate, mutation_rate, hybrid_individual
        """parameters.append(int(args['population_ga']))
        parameters.append(int(args['generation_ga']))
        parameters.append(int(float(args['elitism_ga']) * int(args['population_ga'])))
        parameters.append(float(args['crossover_ga']))
        parameters.append(float(args['mutation_ga']))"""
        
        parameters.append(int(args[0]))
        parameters.append(int(args[1]))
        parameters.append(float(args[2]))
        parameters.append(float(args[3]))
        parameters.append(int(float(args[4]) * parameters[0]))
        parameters.append(None)
        # fitness_list, bits_values, real_values, func_value
        all_results, bits_best, decimal_best, value_best = _GA.GA(parameters).solve(function_object)
        return (time.time() - x), all_results, bits_best, decimal_best, value_best
        
    elif method_id == 2:
        """ parameters.append(int(args['t_sa']))
        parameters.append(float(args['alpha_sa']))
        parameters.append(float(args['tolerance_sa']))
        parameters.append(int(args['iter_sa']))"""
        parameters.append(int(args[0]))
        parameters.append(float(args[1]))
        parameters.append(float(args[2]))
        parameters.append(int(args[3]))
        parameters.append(None)
        fitness_list, bits_values, real_values, func_value = _SA.SA(parameters).solve(function_object)
    return [(time.time() - x), fitness_list, bits_values, real_values, func_value]
    
    """if function_selected_object.multidimensional: del real_values[0]"""
    