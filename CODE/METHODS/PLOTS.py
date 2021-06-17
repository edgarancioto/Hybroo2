import io
import numpy as np
from base64 import b64encode
from matplotlib import cm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sympy.plotting import plot3d
from sympy.plotting.plot import Plot, ContourSeries


class PLots():
    plt.rcParams.update({'font.size': 16})
    plt.rcParams.update({'figure.max_open_warning': 0})

    def plot_function3d(cls, function_object):
        if function_object.dimensions == 2:
            plot_3d = plot3d(function_object.formulation, ('x', function_object.domain[0][0], function_object.domain[0][1]),
                            ('y', function_object.domain[1][0], function_object.domain[1][1]), show=False)
            
            plot_contour = Plot(ContourSeries(function_object.formulation, ('x', function_object.domain[0][0], function_object.domain[0][1]),
                                            ('y', function_object.domain[1][0], function_object.domain[1][1])))
            pl_3d = cls.convert_fig_sympy(plot_3d)
            pl_contour = cls.convert_fig_sympy(plot_contour)
        else:
            x = list(range(-32, 32, 2))
            y = list(range(-32, 32, 2))
            x, y = np.meshgrid(x, y)
            z = []
            for i in range(len(x)):
                for j in range(len(x[i])):
                    z.append(function_object.calculate_to_print_n([x[i][j], y[i][j]]))
            x = np.array(x)
            y = np.array(y)
            z = np.array(z)
            z = z.reshape((len(x), len(y)))
            fig = plt.figure(figsize=(6.4, 4.8))
            print(x, y, z)
            try:
                fig.gca(projection='3d').plot_surface(x, y, z, cmap=cm.viridis, linewidth=0, antialiased=False)
                pl_3d = cls.convert_fig_mat()
            except:
                pl_3d = 'The graph could not be generated.'
            try:
                fig.gca(projection='3d').contour(x, y, z, cmap=cm.viridis, antialiased=False)
                pl_contour = cls.convert_fig_mat()
            except:
                pl_contour = 'The graph could not be generated.'
        
        return pl_3d, pl_contour

    def plot_err(cls, fitness_list_1, fitness_list_2 = None):
        plt.figure(figsize=(10, 10))
        plt.grid(True)
        plt.ylabel('Solution')
        plt.xlabel('Iterations')
        plt.plot(fitness_list_1, linestyle='--', color='blue', linewidth=3)
        err1 = cls.convert_fig_mat()

        if fitness_list_2 is None:
            return err1
    
        plt.figure(figsize=(10, 10))
        plt.grid(True)
        plt.ylabel('Solution')
        plt.xlabel('Iterations')
        plt.plot(fitness_list_2, linestyle='--', color='orange', linewidth=3)
        err2 = cls.convert_fig_mat()
        
        plt.figure(figsize=(10, 10))
        plt.grid(True)
        plt.ylabel('Solution')
        plt.xlabel('Iterations')
        plt.plot(fitness_list_1+fitness_list_2, linestyle='--', color='orange', linewidth=3)
        plt.plot(fitness_list_1, linestyle='--', color='blue', linewidth=3)
        
        if fitness_list_1[-1] > fitness_list_2[-1]:
            plt.annotate('%.3f' % fitness_list_2[-1], (len(fitness_list_1 + fitness_list_2), fitness_list_2[-1]),
                xytext=(-100, 90), textcoords='offset points', bbox=dict(boxstyle="round", fc="0.8"),
                arrowprops=dict(arrowstyle="->", connectionstyle="angle,angleA=0,angleB=90,rad=10"))
        else:
            plt.annotate('%.3f' % fitness_list_1[-1], (len(fitness_list_1), fitness_list_1[-1]), xytext=(-100, 90),
                textcoords='offset points', bbox=dict(boxstyle="round", fc="0.8"), 
                arrowprops=dict(arrowstyle="->", connectionstyle="angle,angleA=0,angleB=135,rad=10"))
        err3 = cls.convert_fig_mat()
        return [err1, err2, err3]

    def convert_fig_mat(cls):
        pic_IObytes = io.BytesIO()
        plt.savefig(pic_IObytes,  format='png')
        pic_IObytes.seek(0)
        pic_hash = b64encode(pic_IObytes.read())
        plt.clf()
        return str(pic_hash)

    def convert_fig_sympy(cls, plot_3d):
        pic_IObytes = io.BytesIO()
        plot_3d.save(pic_IObytes)
        pic_IObytes.seek(0)
        pic_hash = b64encode(pic_IObytes.read())
        plt.clf()
        return str(pic_hash)

    def plot_tsp_path(coord, path, order, title=None):
        plt.clf()
        plt.figure(figsize=(6.4, 4.8))
        x = []
        y = []
        x1 = []
        x2 = []
        for i in range(len(coord)):
            x.append(coord[i][0])
            y.append(coord[i][1])
            x1.append(coord[path[i]][0])
            x2.append(coord[path[i]][1])
        x1.append(x1[0])
        x2.append(x2[0])
        plt.plot(x1, x2, 'co')
        plt.plot(x1, x2)
        plt.axis('off')
        if title is not None:
            plt.title(title)
        save_fig("path" + str(order))

    def plot_vrp_routs(routes, coord, path, order, title=None):
        plt.clf()
        plt.figure(figsize=(6.4, 4.8))
        x = []
        y = []
        starts = 0
        for i in routes:
            for j in range(starts, (starts + i)):
                x.append(coord[path[j]][0])
                y.append(coord[path[j]][1])
                plt.text(x[-1], y[-1], str(path[j]))
            starts += i
        starts = 0
        for i in range(len(routes)):
            x1 = [coord[0][0]] + x[starts:starts + routes[i]] + [coord[0][0]]
            y1 = [coord[0][1]] + y[starts:starts + routes[i]] + [coord[0][1]]
            plt.plot(x1, y1)
            starts += routes[i]
        x.append(coord[0][0])
        y.append(coord[0][1])
        plt.plot(x, y, 'co')
        plt.axis('off')
        if title is not None:
            plt.suptitle(title)
        save_fig("route" + str(order))
