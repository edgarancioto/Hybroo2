from sympy import sympify, latex, Symbol
from sympy.utilities.lambdify import lambdify, lambdastr
from sympy.abc import x

import ast


class Function(object):
    def __init__(self):
        self.id = None
        self.name = None
        self.formulation = None
        self.formulation_original = None
        self.dimensions = 0
        self.domain = None
        self.location = None
        self.best = None
        self.constants = None
        self.descriptions = None
        self.multidimensional = False

    def __str__(self):
        return """Id: %s \nName: %s \nFormulation : %s \nDimensions: %s \nDomain: %s \nLocation: %s \nBest: %s \nParameters: %s \nDescription: %s \n""" % \
               (self.id, self.name, self.formulation, self.dimensions, self.domain, self.location, self.best, self.constants, self.description)

    def build_function(self, data_function):
        self.id = data_function['id']
        self.name = data_function['name']
        self.description = data_function['description']
        self.formulation = data_function['formulation']
        self.constants = None if data_function['constants'] =='None' else data_function['constants']
        self.domain = data_function['domain']
        self.location = data_function['location']
        self.best = data_function['best']

        self.dimensions = self.convert_value(self.description.split(',')[0].split('-')[0])
        
        if self.constants is not None:
            self.constants = ast.literal_eval(self.constants)
            for i in self.constants:
                self.constants[i] = self.convert_value(self.constants[i])

        self.best = self.convert_value(self.best)
        self.domain = self.browse_vector(self.domain, self.dimensions)
        self.location = self.browse_vector(self.location, self.dimensions)

        if self.dimensions == Symbol('n') or self.dimensions > 3:
            self.multidimensional = True
            self.formulation = self.formulation.replace('x[', "IndexedBase('x')[")

        self.formulation = sympify(self.formulation, evaluate=False)

        if self.constants is not None:
            for i in self.constants:
                self.formulation = self.formulation.subs(i, self.constants[i])

        self.formulation_original = self.formulation.copy()

    @staticmethod
    def browse_vector(vector, dimensions):
        try:
            vector = ast.literal_eval(vector)
        except ValueError:
            vector = sympify(vector)

        values = []
        for i in vector:
            values.append(Function.convert_value(i))
        if type(values[0]) is not list and type(dimensions) is int:
            return [values] * dimensions
        else:
            return values

    @staticmethod
    def convert_value(value):
        try:
            return ast.literal_eval(value)
        except Exception:
            return sympify(value)

    def get_domain(self, index):
        return self.domain[index]

    def get_format_expression(self):
        return latex(self.formulation_original)

    def set_n_dimension(self, n):
        self.dimensions = int(n)
        self.formulation = self.formulation.subs('n', n)
        self.domain = self.browse_vector(self.domain, self.dimensions)
        self.location = self.browse_vector(self.location, self.dimensions)

    def calculate(self, v):
        value = self.formulation
        if self.dimensions == Symbol('n') or self.dimensions <= 3:
            for index, val in enumerate(self.formulation.free_symbols):
                try:
                    value = value.subs(val, v[index])
                except Exception as e:
                    print(value, val, v[index], e)
                    return float('inf')
            return float(value)
        else:
            v.insert(0, None)
            value = lambdify(Symbol('x'), value, ("math", "mpmath", "numpy", "sympy"))
            return value(v)

    def calculate_to_print_n(self, v):
        value = self.formulation_original.subs('n', 2)
        try:
            v.insert(0, None)
            value = lambdify(Symbol('x'), value, ("math", "mpmath", "numpy", "sympy"))
            return value(v)
        except Exception as e:
            return float('inf')
