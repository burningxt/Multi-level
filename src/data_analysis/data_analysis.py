from src.multi_level.multi_level import MultiLevel
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np


class DataAnalysis:
    def __init__(self):
        self.dim_set = [10]
        self.problem_set = [1, 2, 5, 9, 10, 11]
        self.columns = ['C' + str(_) for _ in self.problem_set]
        self.number_of_runs = 51
        self.samples = [0]
        self.value_names = ['best', 'worst', 'mean', 'median', 'std']

    def run(self, count):
        for dimension in self.dim_set:
            f_min = np.zeros((1, len(self.problem_set)))
            for problem_id in self.problem_set:
                matrix = np.loadtxt("./benchmarks/input_data/M_{}_D{}.txt".format(problem_id, dimension)).tolist()
                o_shift = np.loadtxt("./benchmarks/input_data/shift_data_{}.txt".format(problem_id)).tolist()
                f_min[0, self.problem_set.index(problem_id)] = \
                    MultiLevel(problem_id, dimension, o_shift, matrix).evolution()
            df = pd.DataFrame(f_min, columns=['C' + str(_) for _ in self.problem_set], index=[count])
            df.to_csv('./data_analysis/outputs/{}D_run{}.csv'.format(dimension, count + 1))

    def append_csv(self, dimension):
        lst_df = []
        for count in range(self.number_of_runs):
            lst_df.append(pd.read_csv('./data_analysis/outputs/{}D_run{}.csv'\
                                      .format(dimension, count + 1), index_col=[0]))
            os.remove('./data_analysis/outputs/{}D_run{}.csv'\
                      .format(dimension, count + 1))
        df = pd.concat(lst_df)
        df.to_csv('./data_analysis/outputs/{}D.csv'\
                  .format(dimension))

    def statistical_analysis(self, dimension):
        arr = np.zeros((5, len(self.problem_set)))
        df = pd.read_csv('./data_analysis/outputs/{}D.csv'\
                         .format(dimension), index_col=[0])
        best = df.min()
        worst = df.max()
        mean = df.mean()
        median = df.median()
        std_variance = df.std()
        arr[0, :] = best[:]
        arr[1, :] = worst[:]
        arr[2, :] = mean[:]
        arr[3, :] = median[:]
        arr[4, :] = std_variance[:]
        df = pd.DataFrame(arr, columns=['C' + str(_) for _ in self.problem_set], index=self.value_names)
        df.to_csv('./data_analysis/outputs/{}D_statistical.csv'\
                  .format(dimension))

    def data_analysis(self):
        for dim in self.dim_set:
            self.append_csv(dim)
            self.statistical_analysis(dim)

    # def bar_chart(self):
    #     for dim in self.dim_set:
    #         for i in self.samples:
    #             for j in self.poisson_values:
    #                 self.append_csv(dim, i, j)
    #                 self.statistical_analysis(dim, i, j)
    #     for column in self.columns:
    #         for dim in self.dim_set:
    #             lst_df = []
    #             for i in self.samples:
    #                 for j in self.poisson_values:
    #                     sample = pd.read_csv('./data_analysis/outputs/{}D_statistical_{}samples_{}poisson.csv'\
    #                                          .format(dim, i, j), index_col=[0])
    #                     sample_mean = sample.loc[['mean'], column]
    #                     lst_df.append(sample_mean)
    #             df = pd.concat(lst_df)
    #             df_transposed = df.T
    #             df_transposed_mean = df_transposed
    #             df_transposed_mean.plot.bar()
    #             plt.savefig('./data_analysis/outputs/figs/mean_{}D_{}.png'\
    #                         .format(dim, column), dpi=1000)
    #             plt.show()



