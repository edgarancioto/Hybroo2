from CODE.METHODS.FUNCTIONS import _GA, _SA
from CODE.METHODS.INSTANCES import TSP_ACO, TSP_GA, TSP_SA, CVRP_ACO, CVRP_GA, CVRP_SA
from CODE.METHODS.PLOTS import PLots
import time

function_object = None
data_function = None

instance_object = None
data_instance = None


def prepare_resolution_instances(instance_name, isHybrid, dp):
    global instance_object, data_instance
    instance_object = load_instance(instance_name)
    data_instance = dp

    initial_time = time.time()
    result_first = recognize_methods_instances(1)

    result_first_done = {'nodes-best': str(result_first[0]), 'value-best': str(result_first[1]), 'time': str(time.time() - initial_time)}
    
    if isHybrid:
        initial_time = time.time()
        result_second = recognize_methods_instances(2, result_first[0])

        result_second_done = {'nodes-best': str(result_first[0]), 'value-best': str(result_first[1]), 'time': str(time.time() - initial_time)}
        
    PLOTS = PLots()

    
    if not isHybrid:
        err1 = PLOTS.plot_err(result_first[1])
        return {
            'problem':function_object.name,
            'problem-description':str(function_object),
            'isHybrid':isHybrid,
            'result-first':result_first_done,
            '3d': pl_3d,
            'contour': pl_contour,
            'err1':err1
        }

    err1, err2, err3 = PLOTS.plot_err(result_first[1], result_second[1])
    
    return {
        'problem':function_object.name,
        'problem-description':str(function_object),
        'isHybrid':isHybrid,
        'result-first':result_first_done,
        'result-second':result_second_done,
        '3d': pl_3d,
        'contour': pl_contour,
        'err1':err1,
        'err2':err2,
        'err3':err3,
        'hibridization-analysis':str('The FIRST hit the value SOMEVALUE in TIME seconds.\nStarting on the best found value, the SECOND *CONDITION got a improve DIFFERENCE in the solution, in TIME seconds. Hybridization reached a value of FINAL-VALUE in a total of FINAL-TIME seconds, considered a effective result, because one method support the other.')
    }

def load_instance(instance_name):
    instance_object = Instance()
    instance_object.load_instance(instance_name)

def recognize_methods_instances(order, hybrid_individual = None):
    results = []
    if order == 1:
        for i in data_function['firstMethod']:
            if i['label'] == 'first-method':
                if i['value'] == 'ga':
                    results = execute_ga(data_function['firstMethod'], hybrid_individual)
                elif i['value'] == 'tsp-sa':
                    results = execute_tsp_sa(data_function['firstMethod'], hybrid_individual)
    else:
        for i in data_function['secondMethod']:
            if i['label'] == 'second-method':
                if i['value'] == 'ga':
                    results = execute_ga(data_function['secondMethod'], hybrid_individual)
                elif i['value'] == 'sa':
                    results = execute_sa(data_function['secondMethod'], hybrid_individual)
    return results
    
    
    instance_type = data_instance['instance_type']
    if instance_type == 'vrp':
        time, path, routes, cost, coordinates, fitness_list = execute_vrp.execute_some_method(instance, method_selected, parameters)
        prepare_results_vrp(1, method_selected, path, routes, coordinates, fitness_list)

        if type_of_method == 'hybrid':
            _, _, method_selected2, parameters = take_parameters_instance(2, args, path)
            time2, path2, routes2, cost2, _, fitness_list = execute_vrp.execute_some_method(instance, method_selected2, parameters)
            prepare_results_vrp(2, method_selected2, path2, routes2, coordinates, fitness_list)
            return type_of_method, instance_type, instance, [method_selected, method_selected2], [time, time2], [cost, cost2]

        return type_of_method, instance_type, instance, method_selected, time, cost

    else:
        time, path, cost, coordinates, fitness_list = execute_tsp.execute_some_method(instance, method_selected, parameters)
        prepare_results_tsp(1, method_selected, path, coordinates, fitness_list)

        if type_of_method == 'hybrid':
            _, _, method_selected2, parameters = take_parameters_instance(2, args, path)
            time2, path2, cost2, _, fitness_list = execute_tsp.execute_some_method(instance, method_selected2, parameters)
            prepare_results_tsp(2, method_selected2, path2, coordinates, fitness_list)
            return type_of_method, instance_type, instance, [method_selected, method_selected2], [time, time2], [cost, cost2]

        return type_of_method, instance_type, instance, method_selected, time, cost



def execute_tsp_sa(params, hybrid_individual = None):
    parameters = [None] * 4
    for i in params:
        if i['label'] == 'T':
            parameters[0] =  int(i['value'])
        if i['label'] == 'Alpha':
            parameters[1] =  float(i['value'])
        if i['label'] == 'Tolerance':
            parameters[2] =  float(i['value'])
        if i['label'] == 'Iterations':
            parameters[3] =  int(i['value'])
    parameters.append(hybrid_individual)
    return TSP_SA.SA(parameters).solve(instance_object)

###############

def prepare_resolution_functions(fo, isHybrid, dp):
    global function_object, data_function
    function_object = fo
    data_function = dp
    print(data_function)
    initial_time = time.time()
    result_first = recognize_methods_functions(1)
    final_time = time.time() - initial_time
    result_first_done = {'decimal-best': {}, 'value-best': str(result_first[3]), 'time': str(final_time)}
    
    j = 1
    for i in result_first[2]:
        result_first_done['decimal-best'][j] = str(i)
        j += 1
    
    if isHybrid:
        initial_time = time.time()
        result_second = recognize_methods_functions(2, result_first[0])
        final_time = time.time() - initial_time
        result_second_done = {'decimal-best': {}, 'value-best': str(result_second[3]), 'time': str(final_time)}
        
        j = 1
        for i in result_second[2]:
            result_second_done['decimal-best'][j] = str(i)
            j += 1
    
    PLOTS = PLots()

    pl_3d, pl_contour = PLOTS.plot_function3d(function_object)
    
    if not isHybrid:
        err1 = PLOTS.plot_err(result_first[1])
        return {
            'problem':function_object.name,
            'problem-description':str(function_object),
            'isHybrid':isHybrid,
            'result-first':result_first_done,
            '3d': pl_3d,
            'contour': pl_contour,
            'err1':err1
        }

    err1, err2, err3 = PLOTS.plot_err(result_first[1], result_second[1])
    
    return {
        'problem':function_object.name,
        'problem-description':str(function_object),
        'isHybrid':isHybrid,
        'result-first':result_first_done,
        'result-second':result_second_done,
        '3d': pl_3d,
        'contour': pl_contour,
        'err1':err1,
        'err2':err2,
        'err3':err3,
        'hibridization-analysis':str('The FIRST hit the value SOMEVALUE in TIME seconds.\nStarting on the best found value, the SECOND *CONDITION got a improve DIFFERENCE in the solution, in TIME seconds. Hybridization reached a value of FINAL-VALUE in a total of FINAL-TIME seconds, considered a effective result, because one method support the other.')
    }

def recognize_methods_functions(order, hybrid_individual = None):
    results = []
    if order == 1:
        for i in data_function['firstMethod']:
            if i['label'] == 'first-method':
                if i['value'] == 'ga':
                    results = execute_ga(data_function['firstMethod'], hybrid_individual)
                elif i['value'] == 'sa':
                    results = execute_sa(data_function['firstMethod'], hybrid_individual)
    else:
        for i in data_function['secondMethod']:
            if i['label'] == 'second-method':
                if i['value'] == 'ga':
                    results = execute_ga(data_function['secondMethod'], hybrid_individual)
                elif i['value'] == 'sa':
                    results = execute_sa(data_function['secondMethod'], hybrid_individual)
    return results
    
def execute_ga(params, hybrid_individual = None):
    parameters = [None] * 5
    for i in params:
        if i['label'] == 'Population':
            parameters[0] =  int(i['value'])
        if i['label'] == 'Generation':
            parameters[1] =  int(i['value'])
        if i['label'] == 'Crossover':
            parameters[2] =  float(i['value'])
        if i['label'] == 'Mutation':
            parameters[3] =  float(i['value'])
        if i['label'] == 'Elitism':
            parameters[4] =  float(i['value'])
    parameters[4] =  int(parameters[4] * parameters[0])
    parameters.append(hybrid_individual)
    return _GA.GA(parameters).solve(function_object)

def execute_sa(params, hybrid_individual = None):
    parameters = [None] * 4
    for i in params:
        if i['label'] == 'T':
            parameters[0] =  int(i['value'])
        if i['label'] == 'Alpha':
            parameters[1] =  float(i['value'])
        if i['label'] == 'Tolerance':
            parameters[2] =  float(i['value'])
        if i['label'] == 'Iterations':
            parameters[3] =  int(i['value'])
    parameters.append(hybrid_individual)
    return _SA.SA(parameters).solve(function_object)
