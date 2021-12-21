#
#
#
import random
from math import tan, pi, sqrt, log, sin, exp
import numpy as np


class Utils:
    @staticmethod
    def individual_swap(ind_1, ind_2):
        ind_1.obj, ind_2.obj = ind_2.obj, ind_1.obj
        ind_1.x, ind_2.x = ind_2.x, ind_1.x
        ind_1.strategy_pb, ind_2.strategy_pb = ind_2.strategy_pb, ind_1.strategy_pb

    @staticmethod
    def individual_copy(ind_1, ind_2):
        ind_1.obj = ind_2.obj
        ind_1.x[:] = ind_2.x[:]
        # ind_1.strategy_pb[:] = ind_2.strategy_pb[:]

    @staticmethod
    def init_strategy_probabilities(number_of_populations, pop_id):
        if pop_id == 0 or pop_id == number_of_populations - 1:
            pb = np.full(3, 1.0 / 3.0)
        else:
            pb = np.full(4, 0.25)
        return pb

    @staticmethod
    def restart_strategy_probabilities(pb, number_of_populations, pop_id):
        if pop_id == 0 or pop_id == number_of_populations - 1:
            # np.resize(pb, 3)
            for _ in range(3):
                pb[_] = 1.0 / 3.0
        else:
            # np.resize(pb, 4)
            for _ in range(4):
                pb[_] = 0.25

    @staticmethod
    def init_strategy_id_list(number_of_populations, pop_id):
        if pop_id == 0 or pop_id == number_of_populations - 1:
            lst_strategy_id = np.arange(3)
        else:
            lst_strategy_id = np.arange(4)
        return lst_strategy_id

    def mixed_strategy(self, pb, strategy_id, pop_id, number_of_populations, is_success, gain):
        sigma = 0.9
        is_restart = False
        if is_success:
            pb[strategy_id] += sigma * gain
        sum_pb = sum(pb) + 0.1
        for j in range(len(pb)):
            pb[j] = (pb[j] + 0.1 / len(pb)) / sum_pb
            if pb[j] < 0.005:
                is_restart = True
                break
        if is_restart:
            self.restart_strategy_probabilities(pb, number_of_populations, pop_id)

    @staticmethod
    def poisson_random(expected_value):
        n = 0
        limit = exp(-expected_value)
        rand = random.random()
        while rand > limit:
            n += 1
            rand *= random.random()
        return n

    @staticmethod
    def rand_cauchy(mu, gamma):
        uniform = random.random()
        z = mu + gamma * tan(pi * (uniform - 0.5))
        return z

    @staticmethod
    def rand_normal(mu, sigma):
        uniform = random.random()
        z = sqrt(- 2.0 * log(uniform)) * sin(2.0 * pi * uniform)
        z = mu + sigma * z
        return z

    def get_mu(self, rand_value, gamma):
        mu = self.rand_cauchy(rand_value, gamma)
        while mu < 0.0:
            mu = self.rand_cauchy(rand_value, gamma)
        return mu

    def get_cr(self, rand_value, gamma):
        cr = self.rand_cauchy(rand_value, gamma)
        while cr < 0.5:
            cr = 0.5
        if cr > 0.5:
            cr = 0.5
        return cr
