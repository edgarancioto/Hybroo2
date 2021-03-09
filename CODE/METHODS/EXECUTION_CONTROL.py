from CODE.METHODS.FUNCTIONS import _GA, _SA
from CODE.METHODS import PLOTS
import time

function_object = None
data_post = None

def execute_control(fo, isHybrid, dp):
    global function_object, data_post
    function_object = fo
    data_post = dp

    initial_time = time.time()
    result_first = prepare_parameters(1)
    final_time = time.time() - initial_time
    result_first_done = {'all-results': {}, 'bits-best': {}, 'decimal-best': {}, 'value-best': str(result_first[3]), 'time': str(final_time)}
    j = 1
    for i in result_first[0]:
        result_first_done['bits-best'][j] = str(i)
        j += 1
    j = 1
    for i in result_first[2]:
        result_first_done['decimal-best'][j] = str(i)
        j += 1
    j = 1
    for i in result_first[1]:
        result_first_done['all-results'][j] = str(i)
        j += 1
    
    if isHybrid:
        initial_time = time.time()
        result_second = prepare_parameters(2, result_first[0])
        final_time = time.time() - initial_time
        result_second_done = {'all-results': {}, 'bits-best': {}, 'decimal-best': {}, 'value-best': str(result_second[3]), 'time': str(final_time)}
        j = 1
        for i in result_second[0]:
            result_second_done['bits-best'][j] = str(i)
            j += 1
        j = 1
        for i in result_second[2]:
            result_second_done['decimal-best'][j] = str(i)
            j += 1
        j = 1
        for i in result_second[1]:
            result_second_done['all-results'][j] = str(i)
            j += 1
    
    pl_3d, pl_contour = PLOTS.plot_function3d(function_object)
    if not isHybrid:
        err1 = PLOTS.plot_err(result_first[1])
        return {
            'result-first':result_first_done,
            'result-second':result_second_done,
            '3d': pl_3d,
            'contour': pl_contour,
            'err1':err1
        }
    err1, err2, err3 = PLOTS.plot_err(result_first[1], result_second[1])
    return {
        'result-first':result_first_done,
        'result-second':result_second_done,
        '3d': pl_3d,
        'contour': pl_contour,
        'err1':err1,
        'err2':err2,
        'err3':err3
    }
    
    
    

def prepare_parameters(order, hybrid_individual = None):
    results = []
    if order == 1:
        for i in data_post['firstMethod']:
            if i['label'] == 'first-method':
                if i['value'] == 'ga':
                    results = prepare_execute_ga(data_post['firstMethod'], hybrid_individual)
                elif i['value'] == 'sa':
                    results = prepare_execute_sa(data_post['firstMethod'], hybrid_individual)
    else:
        for i in data_post['secondMethod']:
            if i['label'] == 'second-method':
                if i['value'] == 'ga':
                    results = prepare_execute_ga(data_post['secondMethod'], hybrid_individual)
                elif i['value'] == 'sa':
                    results = prepare_execute_sa(data_post['secondMethod'], hybrid_individual)
    return results
    
def prepare_execute_ga(params, hybrid_individual = None):
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

def prepare_execute_sa(params, hybrid_individual = None):
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

