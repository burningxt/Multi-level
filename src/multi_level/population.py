#
#
#
from src.multi_level.constant import subpop_size, number_of_populations
from src.benchmarks.cec14 import Cec14
from src.multi_level.individual import Individual
from src.multi_level.utils import Utils
import random
import numpy as np


class Population(Cec14):
    def __init__(self, problem_id, dimension, o_shift, matrix):
        super().__init__(problem_id, dimension, o_shift, matrix)

    def init_population(self):
        """
        Initialize a number 'number_of_populations' of populations with same size 'subpop_size';
        Then, rank them as a whole.
        :return: the whole population
        """
        total_size = number_of_populations * subpop_size
        _pop = []
        for i in range(total_size):
            x = np.zeros(self.dimension)
            Cec14(self.problem_id, self.dimension, self.o_shift, self.matrix).get_param(x)
            obj = Cec14(self.problem_id, self.dimension, self.o_shift, self.matrix).evaluate(x)
            _pop.append(Individual(x, obj))
        _pop.sort(key=lambda ind: ind.obj)
        pop = []
        for i in range(number_of_populations):
            temp = []
            for j in range(subpop_size):
                _pop[i * subpop_size + j].strategy_pb \
                    = Utils().init_strategy_probabilities(number_of_populations, i)[:]
                temp.append(_pop[i * subpop_size + j])
            pop.append(temp)
        return pop

    def init_empty_child(self):
        child = Individual(x=np.zeros(self.dimension), obj=0.0)
        return child

    # def get_center_point(self, p, number_of_ind):
    #     x_center = np.zeros(self.dimension)
    #     ind = random.sample(p, number_of_ind)
    #     for i in range(self.dimension):
    #         sum_of_ind_x = 0
    #         for j in range(number_of_ind):
    #             sum_of_ind_x += ind[j].x[i]
    #         x_center[i] = sum_of_ind_x / number_of_ind
    #     return x_center

    def get_center_point(self, p, ind_current, number_of_ind):
        x_center = np.zeros(self.dimension)
        weights = np.zeros(number_of_ind)
        increments = np.zeros(number_of_ind)
        lst_ind = random.sample(p, number_of_ind)
        t = 0
        while ind_current.obj in [ind.obj for ind in lst_ind] and t < 10:
            lst_ind = random.sample(p, number_of_ind)
            t += 1
        sum_of_ind_x = 0.0
        for i in range(number_of_ind):
            increments[i] = abs(ind_current.obj - lst_ind[i].obj)
        max_increment = increments.max()
        for i in range(number_of_ind):
            sum_of_ind_x += np.e**((ind_current.obj - lst_ind[i].obj) / max_increment)
        for i in range(number_of_ind):
            weights[i] = np.e**((ind_current.obj - lst_ind[i].obj) / max_increment) / sum_of_ind_x
        for j in range(self.dimension):
            for i in range(number_of_ind):
                x_center[j] += weights[i] * lst_ind[i].x[j]
        return x_center

    # @staticmethod
    # def migration(pop, pop_id, is_replaced):
    #     if is_replaced:
    #         insert_position_pop = pop_id
    #         while True:
    #             if insert_position_pop == 0:
    #                 break
    #             else:
    #                 if pop[insert_position_pop][0].obj < pop[insert_position_pop - 1][subpop_size - 1].obj:
    #                     pop[insert_position_pop][0].obj, pop[insert_position_pop - 1][-1].obj \
    #                         = pop[insert_position_pop - 1][-1].obj, pop[insert_position_pop][0].obj
    #                     pop[insert_position_pop][0].x, pop[insert_position_pop - 1][-1].x \
    #                         = pop[insert_position_pop - 1][-1].x, pop[insert_position_pop][0].x
    #                     insert_position_pop = insert_position_pop - 1
    #                     if insert_position_pop == number_of_populations - 2 or insert_position_pop == 0:
    #                         Utils().restart_strategy_probabilities(pop[insert_position_pop][-1].
    #                                                                strategy_pb, number_of_populations,
    #                                                                insert_position_pop)
    #                         Utils().restart_strategy_probabilities(pop[insert_position_pop + 1][0].
    #                                                                strategy_pb, number_of_populations,
    #                                                                insert_position_pop + 1)
    #                 else:
    #                     break
    #             for j in range(1, subpop_size):
    #                 if pop[insert_position_pop][subpop_size - j].obj \
    #                         < pop[insert_position_pop][subpop_size - j - 1].obj:
    #                     Utils.individual_swap(pop[insert_position_pop][subpop_size - j],
    #                                           pop[insert_position_pop][subpop_size - j - 1])
    #                 else:
    #                     break











# if __name__ == '__main__':
#     problem_id = 1
#     dimension = 10
#     o_shift = np.loadtxt("../benchmarks/input_data/shift_data_{}.txt".format(problem_id)).tolist()
#     matrix = np.loadtxt("../benchmarks/input_data/M_{}_D{}.txt".format(problem_id, dimension)).tolist()
#     pop = Population(problem_id, dimension, o_shift, matrix).init_population()
#     pass
