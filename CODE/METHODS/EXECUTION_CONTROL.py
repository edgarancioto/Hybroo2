from typing import Any
from matplotlib.text import Annotation
from CODE.OBJECTS.INSTANCE import Instance
from CODE.METHODS.FUNCTIONS import _GA, _SA
from CODE.METHODS.INSTANCES import TSP_ACO, TSP_GA, TSP_SA, CVRP_ACO, CVRP_GA, CVRP_SA
from CODE.METHODS.PLOTS import PLots
import time
import os
import json
from app import Main

function_object = None
data_function = None

instance_object = None
data_instance = None

def solve_instances(dp):
    global instance_object, data_instance
    data_instance = dp
    
    isHybrid = data_instance['isHybrid']
    j = json.loads(open(os.path.dirname(__file__) + "/../JSON/instances-methods.json", 'r').read())
    type_problem = callable_method = j[data_instance['firstMethod']['name-method']]['problem-type']
    callable_method = j[data_instance['firstMethod']['name-method']]['callable-method']

    instance_object = Instance()
    instance_object.load_instance(type_problem, data_instance['problem'])
    
    initial_time = time.time()
    result_first = globals()[callable_method](data_instance['firstMethod'], None)
    result_first_done = {'nodes-best': str(result_first[0]), 'value-best': str(result_first[1]), 'time': str(time.time() - initial_time)}
    
    PLOTS = PLots()
    route_plot = PLOTS.plot_route(type_problem, instance_object.node_coord, result_first)

    if not isHybrid:
        err1 = PLOTS.plot_err(result_first[2])
        
        return {
            'problem':instance_object.name,
            'problem-description':str(instance_object),
            'isHybrid':isHybrid,
            'result-first':result_first_done,
            'err1':err1,
            'route-path':route_plot
        }

    initial_time = time.time()
    result_second = globals()[callable_method](data_instance['firstMethod'], result_first[0])
    result_second_done = {'nodes-best': str(result_first[0]), 'value-best': str(result_first[1]), 'time': str(time.time() - initial_time)}
        
    err1, err2, err3 = PLOTS.plot_err(result_first[2], result_second[2])
    route_plot_2 = PLOTS.plot_route(type_problem, instance_object.node_coord, result_second)

    return {
        'problem':instance_object.name,
        'problem-description':str(instance_object),
        'isHybrid':isHybrid,
        'result-first':result_first_done,
        'result-second':result_second_done,
        'err1':err1,
        'err2':err2,
        'err3':err3,
        'route-path-1':route_plot,
        'route-path-2':route_plot_2,
        'hibridization-analysis':str('The FIRST hit the value SOMEVALUE in TIME seconds.\nStarting on the best found value, the SECOND *CONDITION got a improve DIFFERENCE in the solution, in TIME seconds. Hybridization reached a value of FINAL-VALUE in a total of FINAL-TIME seconds, considered a effective result, because one method support the other.')
    }

def execute_cvrp_aco(params, hybrid_individual = None):
    parameters = [None] * 6
    parameters[0] =  int(params['Ants'])
    parameters[1] =  int(params['Generation'])
    parameters[2] =  float(params['Alpha'])
    parameters[3] =  float(params['Beta'])
    parameters[4] =  float(params['Rho'])
    parameters[5] =  float(params['Q'])
    parameters.append(hybrid_individual)
    return CVRP_ACO.ACO(parameters).solve(instance_object)

def execute_cvrp_ga(params, hybrid_individual = None):
    parameters = [None] * 5
    parameters[0] =  int(params['Population'])
    parameters[1] =  int(params['Generation'])
    parameters[2] =  int(float(params['Elitism']) * parameters[0])
    parameters[3] =  float(params['Inverse'])
    parameters[4] =  bool(params['Special'] == "checked")
    parameters.append(hybrid_individual)
    return CVRP_GA.GA(parameters).solve(instance_object)

def execute_cvrp_sa(params, hybrid_individual = None):
    parameters = [None] * 4
    parameters[0] =  int(params['T'])
    parameters[1] =  float(params['Alpha'])
    parameters[2] =  float(params['Tolerance'])
    parameters[3] =  int(params['Iterations'])
    parameters.append(hybrid_individual)
    return CVRP_SA.SA(parameters).solve(instance_object)

def execute_tsp_aco(params, hybrid_individual = None):
    parameters = [None] * 6
    parameters[0] =  int(params['Ants'])
    parameters[1] =  int(params['Generation'])
    parameters[2] =  float(params['Alpha'])
    parameters[3] =  float(params['Beta'])
    parameters[4] =  float(params['Rho'])
    parameters[5] =  float(params['Q'])
    parameters.append(hybrid_individual)
    return TSP_ACO.ACO(parameters).solve(instance_object)
    
def execute_tsp_ga(params, hybrid_individual = None):
    parameters = [None] * 7
    parameters[0] =  int(params['Population'])
    parameters[1] =  int(params['Generation'])
    parameters[2] =  int(float(params['Elitism']) * parameters[0])
    parameters[3] =  float(params['Crossover'])
    parameters[4] =  float(params['Simple'])
    parameters[5] =  float(params['Inverse'])
    parameters[6] =  bool(params['Special'] == "checked")
    parameters.append(hybrid_individual)
    return TSP_GA.GA(parameters).solve(instance_object)

def execute_tsp_sa(params, hybrid_individual = None):
    parameters = [None] * 4
    parameters[0] =  int(params['T'])
    parameters[1] =  float(params['Alpha'])
    parameters[2] =  float(params['Tolerance'])
    parameters[3] =  int(params['Iterations'])
    parameters.append(hybrid_individual)
    return TSP_SA.SA(parameters).solve(instance_object)


def solve_functions(dp):
    global function_object, data_function
    data_function = dp
    _, function_object = Main.find_function_by_id(int(data_function['problem']))
    isHybrid = data_function['isHybrid']

    j = json.loads(open(os.path.dirname(__file__) + "/../JSON/functions-methods.json", 'r').read())
    callable_method = j[data_function['firstMethod']['name-method']]['callable-method']

    initial_time = time.time()
    result_first = globals()[callable_method](data_function['firstMethod'], None)
    result_first_done = {'decimal-best': {}, 'value-best': str(result_first[3]), 'time': str(time.time() - initial_time)}
    
    PLOTS = PLots()
    pl_3d, pl_contour = PLOTS.plot_function3d(function_object)

    j = 1
    for i in result_first[2]:
        result_first_done['decimal-best'][j] = str(i)
        j += 1
    
    if not isHybrid:
        err1 = PLOTS.plot_err(result_first[1])
        return {
            'problem':function_object.name,
            'problem-description':str(function_object),
            'isHybrid':isHybrid,
            'result-first':result_first_done,
            '3d':pl_3d,
            'contour':pl_contour,
            'err1':err1
        }

    initial_time = time.time()
    result_second = globals()[callable_method](data_function['firstMethod'], result_first[0])
    result_second_done = {'decimal-best': {}, 'value-best': str(result_second[3]), 'time': str(time.time() - initial_time)}

    j = 1
    for i in result_second[2]:
        result_second_done['decimal-best'][j] = str(i)
        j += 1

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
    
def execute_ga(params, hybrid_individual = None):
    parameters = [None] * 5
    parameters[0] =  int(params['Population'])
    parameters[1] =  int(params['Generation'])
    parameters[2] =  float(params['Crossover'])
    parameters[3] =  float(params['Mutation'])
    parameters[4] =  float(params['Elitism'])
    parameters[4] =  int(parameters[4] * parameters[0])
    parameters.append(hybrid_individual)
    return _GA.GA(parameters).solve(function_object)

def execute_sa(params, hybrid_individual = None):
    parameters = [None] * 4
    parameters[0] =  int(params['T'])
    parameters[1] =  float(params['Alpha'])
    parameters[2] =  float(params['Tolerance'])
    parameters[3] =  int(params['Iterations'])
    parameters.append(hybrid_individual)
    return _SA.SA(parameters).solve(function_object)
