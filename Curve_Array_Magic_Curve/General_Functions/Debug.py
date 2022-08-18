import numpy as np


def print_array(*args):

    np.set_printoptions(precision=4, formatter={'all': lambda x: '\n' + str(x)}, linewidth=0)

    for i in args:

        print(i)

    np.set_printoptions()
