from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
import os
from sympy.plotting import plot3d
from sympy.plotting.plot import Plot, ContourSeries
import numpy as np


plt.rcParams.update({'font.size': 16})
plt.rcParams.update({'figure.max_open_warning': 0})
fitness_history: []
method_history = ""

# global vars to execute functions
type_method, method_1, method_2 = None, None, None
parameters_1, parameters_2 = [], []
simulation_times = 0

# global vars to simulate vrp
best_cost, second_cost = float('inf'), float('inf')
best_time, best_path, best_routes, best_coord = None, None, None, None
second_time, second_path, second_routes, second_coord = None, None, None, None

# global vars to simulate functions
best_function_value, second_function_value = float('inf'), float('inf')
best_point, second_point = None, None
best_fitness, second_fitness = None, None


def reset_values():
    global type_method, method_1, method_2, parameters_1, parameters_2, simulation_times
    type_method, method_1, method_2 = None, None, None
    parameters_1, parameters_2 = [], []
    simulation_times = 0


def validate_parameters_function(args):
    reset_values()
    global type_method, method_1, method_2, parameters_1, parameters_2, simulation_times
    try:
        method_1 = args['method_selected_1']
        if method_1 == 'Simulated Annealing':
            parameters_1.append(int(args['t_sa']))
            parameters_1.append(float(args['alpha_sa']))
            parameters_1.append(float(args['tolerance_sa']))
            parameters_1.append(int(args['iter_sa']))
        elif method_1 == 'Genetic Algorithm':
            parameters_1.append(int(args['population_ga']))
            parameters_1.append(int(args['generation_ga']))
            parameters_1.append(int(float(args['elitism_ga']) * int(args['population_ga'])))
            parameters_1.append(float(args['crossover_ga']))
            parameters_1.append(float(args['mutation_ga']))
        parameters_1.append(None)

        type_method = args['type_of_method']
        if type_method == 'hybrid':
            method_2 = args['method_selected_2']
            if method_2 == 'Simulated Annealing':
                parameters_2.append(int(args['t_sa']))
                parameters_2.append(float(args['alpha_sa']))
                parameters_2.append(float(args['tolerance_sa']))
                parameters_2.append(int(args['iter_sa']))
            elif method_2 == 'Genetic Algorithm':
                parameters_2.append(int(args['population_ga']))
                parameters_2.append(int(args['generation_ga']))
                parameters_2.append(int(float(args['elitism_ga']) * int(args['population_ga'])))
                parameters_2.append(float(args['crossover_ga']))
                parameters_2.append(float(args['mutation_ga']))
        if args['submit_button'] == 'Simulation':
            simulation_times = int(args['simulation_times'])
    except (KeyError, ValueError):
        type_method, method_1, method_2 = None, None, None
        parameters_1, parameters_2 = [], []
        simulation_times = 0.0
        return False
    return True


def controller_execute_function(function_selected_object):
    plot_function3d(function_selected_object)
    time_1, fitness_list_1, bits_values_1, real_values_1, func_value_1 = execute_function.execute_some_method(function_selected_object, method_1, parameters_1)
    plot_err(fitness_list_1, 1, method_1)
    if type_method == 'hybrid':
        parameters_2.append(bits_values_1)
        time_2, fitness_list_2, _, real_values_2, func_value_2 = execute_function.execute_some_method(function_selected_object, method_2, parameters_2)
        plot_err(fitness_list_2, 2, method_2)
        return type_method, [method_1, method_2], [time_1, time_2], [real_values_1, real_values_2], [func_value_1, func_value_2]
    return type_method, method_1, time_1, real_values_1, func_value_1


def controller_simulate_function_method(function_selected_object):
    times, values = [], []
    update_simulation_function_progress(0, [1], [0])
    plot_function3d(function_selected_object)
    for i in range(simulation_times):
        time_1, fitness_list_1, bits_values_1, real_values_1, func_value_1 = execute_function.execute_some_method(function_selected_object, method_1, parameters_1)
        update_function_bests(func_value_1, time_1, real_values_1, fitness_list_1)
        if type_method == 'hybrid':
            parameters_2.append(bits_values_1)
            time_2, fitness_list_2, _, real_values_2, func_value_2 = execute_function.execute_some_method(function_selected_object, method_2, parameters_2)
            update_function_bests(func_value_2, time_2, real_values_2, fitness_list_1 + fitness_list_2)
            times.append(round(time_1 + time_2, 2))
            values.append(func_value_2)
        else:
            times.append(round(time_1, 2))
            values.append(func_value_1)
        update_simulation_function_progress(i, times, values)
    prepare_results_function_simulation(times, values, method_1, method_2)


# function just for tests in programmer mode
def controller_repetition_function_method(function_selected_object):
    times, fitness_values = [], []

    print("log: Solving the function", function_selected_object.name)
    for i in range(simulation_times):
        print("log: Repetition nº", i)
        time_1, fitness_list_1, bits_values_1, real_values_1, func_value_1 = execute_function.execute_some_method(function_selected_object, method_1, parameters_1)
        if type_method == 'hybrid':
            parameters_2.append(bits_values_1)
            time_2, fitness_list_2, _, real_values_2, func_value_2 = execute_function.execute_some_method(function_selected_object, method_2, parameters_2)
            times.append(round(time_1 + time_2, 2))
            fitness_values.append(fitness_list_2)
        else:
            times.append(round(time_1, 2))
            fitness_values.append(fitness_list_1)
        print("log: Solved function", function_selected_object.name, i, "times")

        file_name = str(method_1)
        if type_method == 'hybrid':
            file_name += "+" + str(method_2)
        file_name += "-" + str(function_selected_object.name)
        save_repetition(file_name, times[-1], fitness_values[-1])


def update_function_bests(function_value, time, point, fitness):
    global best_function_value, second_function_value, best_point, second_point, best_time, second_time, best_fitness, second_fitness
    if function_value < best_function_value:
        second_function_value = best_function_value
        second_time = best_time
        second_point = best_point
        second_fitness = best_fitness
        best_function_value = function_value
        best_time = time
        best_point = point
        best_fitness = fitness
    else:
        if function_value < second_function_value:
            second_function_value = function_value
            second_time = time
            second_point = point
            second_fitness = fitness


def update_simulation_function_progress(count, times, func_values):
    try:
        arq_w = open(os.getcwd() + "/FrontEnd/static/files/simulation-status.txt", "w")
    except FileNotFoundError:
        arq_w = open(os.getcwd() + "/FrontEnd/static/files/simulation-status.txt", "w+")

    if count == 0:
        text = 'starting'
    elif count + 1 == simulation_times:
        text = 'finish'
        text += "\nTimes: " + str(times)
        text += "\nValues: " + str(func_values)
    else:
        text = "Total of simulations: " + str(simulation_times)
        text += "\nExecuted: " + str(count + 1)
        avg = sum(times) / len(times)
        text += "\nAverage Time: " + str(avg)
        text += "\nTime Left: " + str((simulation_times - (count + 1)) * avg)
    arq_w.write(text)
    arq_w.close()


def prepare_results_function_simulation(times, values, method_selected_1, method_selected_2=None):
    plt.boxplot(times, labels=['Time(s)'])
    plt.gca().yaxis.grid(True)
    save_fig("times-boxplot")

    plt.boxplot(values, labels=['Values'])
    plt.annotate('%.2f' % min(values), (1, min(values)), xytext=(40, 0), textcoords='offset points', bbox=dict(boxstyle="round", fc="0.8"),
                 arrowprops=dict(arrowstyle="->", connectionstyle="angle,angleA=90,angleB=0,rad=10"))
    plt.gca().yaxis.grid(True)
    save_fig("values-boxplot")

    plt.figure(figsize=(6.4, 5.4))
    plt.scatter(times, values)
    plt.xlabel('Time(s)')
    plt.ylabel('Values')
    save_fig("scatter")

    global best_function_value, best_time, best_point, best_fitness, second_function_value, second_time, second_point, second_fitness

    if method_selected_2 is not None:
        method = method_selected_1+method_selected_2
    else:
        method = method_selected_1
    plot_err(best_fitness, 1, method, '-simulation-1')
    plot_err(second_fitness, 1, method, '-simulation-2')


# ---------------methods of control operations of instances---------------


def controller_simulate_method(args, simulation_times):
    times, costs = [], []
    method_selected_2, parameters_2 = None, None
    type_of_method = args['type_of_method']

    type_of_problem, instance, method_selected_1, parameters_1 = take_parameters_instance(1, args)
    if type_of_method == 'hybrid':
        _, _, method_selected_2, parameters_2 = take_parameters_instance(2, args)

    update_simulation_progress(0, simulation_times, [1], [0])

    for i in range(simulation_times):
        if type_of_problem == 'vrp':
            time, path, routes, cost, coordinates, _ = execute_vrp.execute_some_method(instance, method_selected_1, parameters_1)
            update_bests(type_of_problem, cost, time, path, coordinates, routes)
        else:
            time, path, cost, coordinates, _ = execute_tsp.execute_some_method(instance, method_selected_1, parameters_1)
            update_bests(type_of_problem, cost, time, path, coordinates)
        if type_of_method == 'hybrid':
            parameters_2[-1] = path
            if type_of_problem == 'vrp':
                time2, path, routes, cost2, _, _ = execute_vrp.execute_some_method(instance, method_selected_2, parameters_2)
                update_bests(type_of_problem, cost2, time2, path, coordinates, routes)
            else:
                time2, path, cost2, _, _ = execute_tsp.execute_some_method(instance, method_selected_2, parameters_2)
                update_bests(type_of_problem, cost2, time2, path, coordinates)

            times.append(round(time + time2, 2))
            costs.append(cost2)
        else:
            times.append(round(time, 2))
            costs.append(cost)
        update_simulation_progress(i, simulation_times, times, costs)

    prepare_results_simulation(type_of_problem, times, costs)


# function just for tests in programmer mode
def controller_repetition_method(args, simulation_times):
    times, fitness_values = [], []
    method_selected_2, parameters_2 = None, None
    type_of_method = args['type_of_method']

    type_of_problem, instance, method_selected_1, parameters_1 = take_parameters_instance(1, args)
    if type_of_method == 'hybrid':
        _, _, method_selected_2, parameters_2 = take_parameters_instance(2, args)

    print("log: Solving the instance", instance, " by methods ", method_selected_1, method_selected_2)
    for i in range(simulation_times):
        if type_of_problem == 'vrp':
            time, path, _, _, _, fitness_list_1 = execute_vrp.execute_some_method(instance, method_selected_1, parameters_1)
        else:
            time, path, _, _, fitness_list_1 = execute_tsp.execute_some_method(instance, method_selected_1, parameters_1)
        if type_of_method == 'hybrid':
            parameters_2[-1] = path
            if type_of_problem == 'vrp':
                time2, _, _, _, _, fitness_list_2 = execute_vrp.execute_some_method(instance, method_selected_2, parameters_2)
            else:
                time2, _, _, _, fitness_list_2 = execute_tsp.execute_some_method(instance, method_selected_2, parameters_2)
            times.append(round(time + time2, 2))
            fitness_values.append(fitness_list_2)
        else:
            times.append(round(time, 2))
            fitness_values.append(fitness_list_1)
        print("log: Solved instance", instance, i, "times")

        file_name = str(method_selected_1)
        if type_of_method == 'hybrid':
            file_name += "+" + str(method_selected_2)
        file_name += "-" + str(instance)
        save_repetition(file_name, times[-1], fitness_values[-1])

def save_repetition(file_name, time, fitness_list):
    file = os.path.dirname(__file__) + "/TestFiles/" + file_name + ".txt"
    try:
        arq_r = open(file, "r")
        text = arq_r.read()
        arq_w = open(file, "w")
        print("log: file exist")
    except FileNotFoundError:
        arq_w = open(file, "w+")
        text = ""
        print("log: creating a new file")

    text += str(time) + "\t" + str(fitness_list) + "\n"
    arq_w.write(text)
    arq_w.close()
    print("log: file saved")

def update_bests(type_of_problem, cost, time, path, coord, routes=None):
    global best_cost, best_time, best_path, best_coord, best_routes, second_cost, second_time, second_path, second_routes, second_coord
    if cost < best_cost:
        second_cost = best_cost
        best_cost = cost
        second_time = best_time
        best_time = time
        second_path = best_path
        best_path = path
        second_coord = best_coord
        best_coord = coord
        if type_of_problem == 'vrp':
            second_routes = best_routes
            best_routes = routes
    else:
        if cost < second_cost:
            second_cost = cost
            second_time = time
            second_path = path
            second_coord = coord
            if type_of_problem == 'vrp':
                second_routes = routes

def update_simulation_progress(count, simulation_times, times, costs):
    try:
        arq_w = open(os.getcwd() + "/FrontEnd/static/files/simulation-status.txt", "w")
    except FileNotFoundError:
        arq_w = open(os.getcwd() + "/FrontEnd/static/files/simulation-status.txt", "w+")

    if count == 0:
        text = 'starting'
    elif count + 1 == simulation_times:
        text = 'finish'
        text += "\nTimes: " + str(times)
        text += "\nCosts: " + str(costs)
    else:
        text = "Total of simulations: "+str(simulation_times)
        text += "\nExecuted: " + str(count + 1)
        avg = sum(times)/len(times)
        text += "\nAverage Time: " + str(avg)
        text += "\nTime Left: " + str((simulation_times - (count + 1)) * avg)
    arq_w.write(text)
    arq_w.close()

def prepare_results_simulation(type_of_problem, times, costs):
    plt.boxplot(times, labels=['Time(s)'])
    plt.gca().yaxis.grid(True)
    save_fig("times-boxplot")

    plt.boxplot(costs, labels=['Cost'])
    plt.annotate('%.2f' % min(costs), (1, min(costs)), xytext=(40, 0), textcoords='offset points', bbox=dict(boxstyle="round", fc="0.8"),
                 arrowprops=dict(arrowstyle="->", connectionstyle="angle,angleA=90,angleB=0,rad=10"))
    plt.gca().yaxis.grid(True)
    save_fig("costs-boxplot")

    plt.figure(figsize=(6.4, 5.4))
    plt.scatter(times, costs)
    plt.xlabel('Time(s)')
    plt.ylabel('Cost')
    save_fig("scatter")

    global best_cost, best_time, best_path, best_coord, best_routes, second_cost, second_time, second_path, second_routes, second_coord

    title_1 = 'Solved in: '+str(round(best_time, 2))+'(s) with the cost: '+str(round(best_cost, 2))
    title_2 = 'Solved in: ' + str(round(second_time, 2)) + '(s) with the cost: ' + str(round(second_cost, 2))

    if type_of_problem == 'vrp':
        plot_vrp_routs(best_routes, best_coord, best_path, '-best', title_1)
        plot_vrp_routs(second_routes, second_coord, second_path, '-second', title_2)
    else:
        plot_tsp_path(best_coord, best_path, '-best', title_1)
        plot_tsp_path(second_coord, second_path, '-second', title_2)