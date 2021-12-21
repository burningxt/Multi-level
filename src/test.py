import numpy as np


class M:
    def __init__(self, pb):
        self.pb = pb


# a = np.array([1, 2, 3, 4])
# b = np.array([5, 6, 7, 8])
a = [1, 2, 3, 4]
b = [5, 6, 7, 8]
ind_1 = M(a)
ind_2 = M(b)
print('ind_1.pb = ', ind_1.pb)
print('ind_2.pb = ', ind_2.pb)
ind_1.pb, ind_2.pb = ind_2.pb, ind_1.pb
# a[:] = b[:]
# b[3] = 9
print('ind_1.pb = ', ind_1.pb)
print('ind_2.pb = ', ind_2.pb)
print(np.arange(4))
