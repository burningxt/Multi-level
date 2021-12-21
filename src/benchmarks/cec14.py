#
#
from math import fmod, sin, sqrt, cos, pi, exp, e
import random


class Cec14:
    def __init__(self, problem_id, dimension, o_shift, matrix):
        self.problem_id = problem_id
        self.dimension = dimension
        self.o_shift = o_shift
        self.matrix = matrix
        self.lb = -100.0
        self.ub = 100.0

    def shift_func(self, x, y):
        for i in range(self.dimension):
            y[i] = x[i] - self.o_shift[i]

    def rotate_func(self, y, z):
        for i in range(self.dimension):
            for j in range(self.dimension):
                z[i] += y[j] * self.matrix[i][j]

    def shift_and_rotate_func(self, x, y, z, shift_rate):
        self.shift_func(x, y)
        for i in range(self.dimension):
            y[i] *= shift_rate
        self.rotate_func(y, z)

    def schwefel_func(self, z):
        f1 = 0.0
        for i in range(self.dimension):
            z[i] += 4.209687462275036e+002
            if abs(z[i]) < 500.0:
                f1 += z[i] * sin(abs(z[i]) ** 0.5)
            elif z[i] > 500.0:
                f1 += (500.0 - fmod(z[i], 500.0)) * sin(sqrt(abs(500.0 - fmod(z[i], 500.0)))) - (z[i] - 500.0) ** 2 / \
                      (10000.0 * self.dimension)
            elif z[i] < -500.0:
                f1 += (fmod(abs(z[i]), 500.0) - 500.0) * sin(sqrt(abs(fmod(abs(z[i]), 500.0) - 500.0))) - \
                      (z[i] + 500.0) ** 2 / \
                      (10000.0 * self.dimension)
        f = 418.9829 * self.dimension - f1
        return f

    def evaluate(self, x):
        y = [0.0] * self.dimension
        z = [0.0] * self.dimension
        f = 0.0
        # if self.problem_id == 1:
        #     for i in range(1, self.dimension):
        #         f += x[i]**2
        if self.problem_id == 1:
            self.shift_and_rotate_func(x, y, z, shift_rate=1.0)
            for i in range(self.dimension):
                f += (10.0 ** 6) ** (i / (self.dimension - 1)) * z[i] ** 2
            # f += 100.0

        elif self.problem_id == 2:
            self.shift_and_rotate_func(x, y, z, shift_rate=1.0)
            f1 = 0.0
            for i in range(1, self.dimension):
                f1 += z[i] ** 2
            for i in range(self.dimension):
                f += z[0] ** 2 + 10.0 ** 6 * f1
            # f += 200

        elif self.problem_id == 5:
            self.shift_and_rotate_func(x, y, z, shift_rate=1.0)
            f1, f2 = 0.0, 0.0
            for i in range(self.dimension):
                f1 += z[i] ** 2
            for i in range(self.dimension):
                f2 += cos(2.0 * pi * z[i])
            for i in range(self.dimension):
                f += -20.0 * exp(-0.2 * sqrt(1.0 / self.dimension * f1)) - exp(1.0 / self.dimension * f2) + 20.0 + e
            # f += 500.0

        elif self.problem_id == 9:
            self.shift_and_rotate_func(x, y, z, shift_rate=5.12 / 100.0)
            for i in range(self.dimension):
                f += z[i] ** 2 - 10.0 * cos(2.0 * pi * z[i]) + 10.0
            # f += 900.0

        elif self.problem_id == 10:
            self.shift_and_rotate_func(x, y, z, shift_rate=10000.0 / 100.0)
            f = self.schwefel_func(z)
            # f += 1000

        elif self.problem_id == 11:
            self.shift_and_rotate_func(x, y, z, shift_rate=10000.0 / 100.0)
            f = self.schwefel_func(z)
            # f += 1100
        return f

    def get_param(self, _x):
        for i in range(self.dimension):
            _x[i] = self.lb + (self.ub - self.lb) * random.random()
