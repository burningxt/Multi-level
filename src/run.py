from src.data_analysis.data_analysis import DataAnalysis
from src.multi_level.multi_level import MultiLevel
# from src.multi_level.multi_level_rand_de import MultiLevel
import timeit
import multiprocessing as mp
import numpy as np
import pandas as pd


# if __name__ == '__main__':
#     __spec__ = "ModuleSpec(name='builtins', loader=<class '_frozen_importlib.BuiltinImporter'>)"
#     start = timeit.default_timer()
#     pool = mp.Pool(processes=26)
#     res = pool.map(DataAnalysis().run, range(51))
#     DataAnalysis().data_analysis()
#     stop = timeit.default_timer()
#     print('Time: ', stop - start)

if __name__ == '__main__':
    __spec__ = "ModuleSpec(name='builtins', loader=<class '_frozen_importlib.BuiltinImporter'>)"
    start = timeit.default_timer()
    problem_id = 9
    dimension = 10
    matrix = np.loadtxt("./benchmarks/input_data/M_{}_D{}.txt".format(problem_id, dimension))
    o_shift = np.loadtxt("./benchmarks/input_data/shift_data_{}.txt".format(problem_id))
    MultiLevel(problem_id, dimension, o_shift, matrix).evolution()
    stop = timeit.default_timer()
    print('Time: ', stop - start)
