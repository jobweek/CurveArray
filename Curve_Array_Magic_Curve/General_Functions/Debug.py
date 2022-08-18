import numpy as np


def print_array(arr):

    np.set_printoptions(precision=4, formatter={'all': lambda x: '\n'+str(x)}, linewidth=0)

    print(arr)

    np.set_printoptions()
