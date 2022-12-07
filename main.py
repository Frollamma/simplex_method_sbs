import numpy as np
from utils import *

'''
Takes in input a linear programming problem in standard form
'''

#def print_tableau(mode, data):
#'''Mode can be \'plain\' or \'latex\''''


# Matrix of technologic coefficents
A = np.array([
    [1, 2, 3],
    [4, 5, 6]
])

# Right-hand sides
b = np.array([1, 2, 3])

# Vector of costs (relative to the linear objective function)
c = np.array([1, 2, 3])

if not is_standard_form(A, b, c):
    raise ValueError('Problem not in standard form')

