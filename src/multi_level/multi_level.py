#
#
#
from src.benchmarks.cec14 import Cec14
from src.multi_level.population import Population
from src.multi_level.search_operators import SearchOperators
from src.multi_level.constant import subpop_size, number_of_populations
from src.multi_level.utils import Utils
import random
import numpy as np
from copy import deepcopy


class MultiLevel(Cec14):
    def __init__(self, problem_id, dimension, o_shift, matrix):
        super().__init__(problem_id, dimension, o_shift, matrix)
        self.Cls_Population = Population(self.problem_id, self.dimension, self.o_shift, self.matrix)
        self.Cls_SearchOperators = SearchOperators(self.problem_id, self.dimension, self.o_shift, self.matrix)

    def multi_level(self, pop, child, i, j):
        lst_strategy_id = Utils.init_strategy_id_list(number_of_populations, i)[:]
        strategy_id = np.random.choice(lst_strategy_id, 1, p=pop[i][j].strategy_pb)[0]
        self.Cls_SearchOperators.strategies(pop, child, i, j, strategy_id)
        child.obj = self.evaluate(child.x)
        child.strategy_pb = Utils().init_strategy_probabilities(number_of_populations, i)[:]
        self.Cls_SearchOperators.selection(pop, child, i, j, strategy_id)

    def evolution(self):
        pop = self.Cls_Population.init_population()
        child = self.Cls_Population.init_empty_child()
        fes = 0
        fes_max = 1000000 * self.dimension
        while fes < fes_max:
            i = random.randint(0, number_of_populations - 1)
            j = random.randint(0, subpop_size - 1)
            self.multi_level(pop, child, i, j)
            fes += 1
            print(fes, pop[0][0].obj)
        return pop[0][0].obj



