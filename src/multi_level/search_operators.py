#
#
#
from src.multi_level.constant import golden, number_of_inds, number_of_populations, subpop_size
from src.benchmarks.cec14 import Cec14
from src.multi_level.utils import Utils
from src.multi_level.population import Population
import random


class SearchOperators(Cec14):
    def __init__(self, problem_id, dimension, o_shift, matrix):
        super().__init__(problem_id, dimension, o_shift, matrix)
        self.golden = 0.38
        self.mu_rand = 2.0
        self.cr_rand = 0.5
        self.gamma = 0.2
        self.sigma = 0.3
        # self.poisson_value = 2
        # self.mu = 0.5 + 0.1 * random.random()

    def x_correction(self, child):
        for _ in range(self.dimension):
            if child.x[_] < self.lb:
                child.x[_] = min(2 * self.lb - child.x[_], self.ub)
            elif child.x[_] > self.ub:
                child.x[_] = max(self.lb, 2 * self.ub - child.x[_])

    def _mutation(self, pop, child, center_id, pop_id, idx, is_downhill):
        ind_1, ind_2 = random.sample(pop[pop_id], 2)
        while ind_1 == pop[pop_id][idx] or ind_2 == pop[pop_id][idx]:
            ind_1, ind_2 = random.sample(pop[pop_id], 2)
        x_center = Population(self.problem_id, self.dimension, self.o_shift, self.matrix).\
            get_center_point(pop[center_id], pop[pop_id][idx], number_of_inds)
        mu = Utils().get_mu(self.mu_rand, self.gamma)
        for _ in range(self.dimension):
            child.x[_] = pop[pop_id][idx].x[_] + self.golden * mu * (x_center[_] - pop[pop_id][idx].x[_]) * is_downhill\
                         + self.golden * mu * (ind_1.x[_] - ind_2.x[_])
            # child.x[_] = pop[pop_id][idx].x[_] + self.golden * Utils.poisson_random(self.poisson_value) \
            #              * (x_center[_] - pop[pop_id][idx].x[_]) * is_downhill
        self.x_correction(child)

    def mutation_current_to_lower(self, pop, child, pop_id, idx):
        center_id = pop_id - 1
        self._mutation(pop, child, center_id, pop_id, idx, 1)

    def mutation_same_level(self, pop, child, pop_id, idx):
        center_id = pop_id
        self._mutation(pop, child, center_id, pop_id, idx, 1)

    def mutation_higher_to_current(self, pop, child, pop_id, idx):
        center_id = pop_id + 1
        self._mutation(pop, child, center_id, pop_id, idx, -1)

    def _crossover_exp(self, pop, child, center_id, pop_id, idx):
        x_center = Population(self.problem_id, self.dimension, self.o_shift, self.matrix). \
            get_center_point(pop[center_id], pop[pop_id][idx], number_of_inds)
        x_center = Population(self.problem_id, self.dimension, self.o_shift, self.matrix). \
            get_center_point(pop[center_id], pop[pop_id][idx], number_of_inds)
        cr = Utils().get_cr(self.cr_rand, self.sigma)
        j_rand = random.randint(0, self.dimension - 1)
        for j in range(self.dimension):
            if j_rand != j and random.random() <= cr:
                child.x[j] = pop[pop_id][idx].x[j]
            else:
                child.x[j] = x_center[j]
        child.obj = self.evaluate(child.x)
        a = sum(child.x)
        b = [sum(pop[center_id][_].x) for _ in range(50)]
        d = child.obj
        f = [pop[center_id][_].obj for _ in range(50)]
        if a in b:
            c = b.index(a)
            c += 0
        if d in f:
            g = f.index(d)
            g += 0

    def crossover_exp(self, pop, child, pop_id, idx):
        center_id = 0
        self._crossover_exp(pop, child, center_id, pop_id, idx)

    def _crossover_bi(self, pop, child, center_id, pop_id, idx):
        x_center = Population(self.problem_id, self.dimension, self.o_shift, self.matrix). \
            get_center_point(pop[center_id], pop[pop_id][idx], number_of_inds)
        cr = Utils().get_cr(self.cr_rand, self.sigma)
        n = random.randint(0, self.dimension - 1)
        l = 0
        for j in range(self.dimension):
            child.x[j] = pop[pop_id][idx].x[j]
        while random.random() <= cr and l < self.dimension:
            child.x[(n + l) % self.dimension] = x_center[[(n + l) % self.dimension]]
            l += 1
        a = sum(child.x)
        b = [sum(pop[center_id][_].x) for _ in range(50)]
        if a in b:
            c = b.index(a)
            c += 0

    def crossover_bi(self, pop, child, pop_id, idx):
        center_id = 0
        self._crossover_bi(pop, child, center_id, pop_id, idx)

    def strategies(self, pop, child, pop_id, idx, strategy_id):
        if pop_id == 0:
            if strategy_id == 0:
                self.mutation_higher_to_current(pop, child, pop_id, idx)
            # elif strategy_id == 1:
            #     self.mutation_same_level(pop, child, pop_id, idx)
            elif strategy_id == 1:
                self.crossover_exp(pop, child, pop_id, idx)
            elif strategy_id == 2:
                self.crossover_exp(pop, child, pop_id, idx)
        elif pop_id == number_of_populations - 1:
            if strategy_id == 0:
                self.mutation_current_to_lower(pop, child, pop_id, idx)
            # elif strategy_id == 1:
            #     self.mutation_same_level(pop, child, pop_id, idx)
            elif strategy_id == 1:
                self.crossover_exp(pop, child, pop_id, idx)
            elif strategy_id == 2:
                self.crossover_exp(pop, child, pop_id, idx)
        else:
            if strategy_id == 0:
                self.mutation_current_to_lower(pop, child, pop_id, idx)
            elif strategy_id == 1:
                self.mutation_higher_to_current(pop, child, pop_id, idx)
            # elif strategy_id == 2:
            #     self.mutation_same_level(pop, child, pop_id, idx)
            elif strategy_id == 2:
                self.crossover_exp(pop, child, pop_id, idx)
            elif strategy_id == 3:
                self.crossover_exp(pop, child, pop_id, idx)

    # @staticmethod
    # def selection(pop, child, pop_id, idx):
    #     is_replaced = False
    #     gain = 0
    #     if pop[pop_id][idx].obj > child.obj:
    #         is_replaced = True
    #         gain = (pop[pop_id][idx].obj - child.obj) / (pop[-1][-1].obj - pop[0][0].obj)
    #     if is_replaced:
    #         Utils().individual_copy(pop[pop_id][idx], child)
    #     return is_replaced, gain

    # def selection(self, pop, child, pop_id, idx, strategy_id):
    #     is_replace = False
    #     jump_level = pop_id
    #     gain = 0
    #     if pop[pop_id][idx].obj > child.obj and pop[pop_id][idx].obj > pop[0][0].obj:
    #         gain = (pop[pop_id][idx].obj - child.obj) / (pop[pop_id][idx].obj - pop[0][0].obj)
    #         is_replace = True
    #     if is_replace:
    #         if pop_id > 0:
    #             for i in range(pop_id):
    #                 if pop[i][-1].obj > child.obj:
    #                     jump_level = i
    #                     break
    #             if jump_level == pop_id:
    #                 Utils().mixed_strategy(child.strategy_pb, strategy_id, jump_level,
    #                                        number_of_populations, is_replace, gain)
    #                 Utils().individual_swap(pop[pop_id][idx], child)
    #                 self.bubbling(pop, jump_level, idx)
    #             else:
    #                 Utils().individual_copy(pop[i][-1], child)
    #                 self.bubbling(pop, jump_level, subpop_size - 1)
    #         else:
    #             Utils().mixed_strategy(child.strategy_pb, strategy_id, jump_level,
    #                                    number_of_populations, is_replace, gain)
    #             Utils().individual_swap(pop[pop_id][idx], child)
    #             self.bubbling(pop, jump_level, idx)

    def selection(self, pop, child, pop_id, idx, strategy_id):
        is_replace = False
        is_replaced = False
        gain = 0
        if pop[pop_id][idx].obj > child.obj:
            gain = (pop[pop_id][idx].obj - child.obj) / (pop[pop_id][-1].obj - pop[0][0].obj)
            is_replace = True
        if is_replace:
            for i in range(pop_id):
                for j in range(subpop_size):
                    if pop[i][j].obj > child.obj:
                        Utils().individual_copy(pop[i][j], child)
                        is_replaced = True
                        break
                if is_replaced:
                    break
            if not is_replaced:
                Utils().mixed_strategy(child.strategy_pb, strategy_id, pop_id,
                                       number_of_populations, is_replace, gain)
                Utils().individual_swap(pop[pop_id][idx], child)
                self.bubbling(pop, pop_id, idx)

    @staticmethod
    def bubbling(pop, pop_id, idx):
        if idx > 0:
            for j in range(idx):
                if pop[pop_id][idx - j - 1].obj > pop[pop_id][idx - j].obj:
                    Utils().individual_swap(pop[pop_id][idx - j - 1], pop[pop_id][idx - j])
                else:
                    break













