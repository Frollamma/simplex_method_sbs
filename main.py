import numpy as np
#import sympy as sp
from utils import *
from sympy.matrices import Matrix
from sympy import Rational, pprint
# from fractions import Fraction

'''
Takes in input a linear programming problem in standard form
'''

def first_negative_item_index(my_list):
    for i in range(len(my_list)):
        if my_list[i] < 0:
            return i
    return -1

def get_base_costs(c, base_indexes):
    return Matrix([c[i] for i in base_indexes]).transpose()

def compute_tableau(A, b, c, base_indexes):
    B = A[:, base_indexes]
    # print('B: ', B)
    invB = B.inv()
    x_B = invB * b
    # print('x_B: ', x_B)
    c_B = get_base_costs(c, base_idx)
    # print('c_B: ', c_B)
    C = invB * A
    # print('C: ', C)
    rc = c - c_B * invB * A # Reduced costs
    # print('rc: ', rc)
    z = - c_B * x_B
    # print('z: ', z)
    return [x_B, z, rc, C]
    
def compose_tableau(x_B, z, reduced_costs, C):
    row = z.row_join(reduced_costs)
    # print('row: ', row)
    tableau = x_B.row_join(C)
    # print('tableau: ', tableau)
    tableau = row.col_join(tableau)
    return tableau

def print_tableau(tableau, mode='plain'):
    '''Mode can be \'plain\' or \'latex\''''
    if mode=='plain':
        pprint(tableau)
    elif mode=='LaTeX':# TEMP - IMPR
        pass


# Matrix of technologic coefficents
A = Matrix([
    [3, -2, 1, 0],
    [1, 0, 0, 1]
])
# A = Matrix([[1, 2, Rational(3, 2)], [4, 5, 6], [7, 23, 5]])

# Right-hand sides
b = Matrix([12, 5])

# Vector of costs (relative to the linear objective function)
c = Matrix([-3, 2, 0, 0]).transpose()

# Indexes of A columns corresponding to the base
base_idx = [2, 3]

m = A.rows
n = A.cols

if not is_standard_form(A, b, c):
    raise ValueError("Problem not in standard form")

if len(base_idx) != m:
    raise ValueError(f"Number of base indexes doesn't match rank of technological coefficients matrix: {m}")

# Starting base matrix
B = A[:, base_idx]

if B.det() == 0:
    raise ValueError("Base matrix non invertible")

max_iterations = 20
counter = 0
while counter < max_iterations:
    [x_B, z, rc, C] = compute_tableau(A, b, c, base_idx)
    tableau = compose_tableau(x_B, z, rc, C)
    print_tableau(tableau)

    # j = np.where(np.asarray(rc) < 0)[0][0]
    j = first_negative_item_index(rc)
    if j == -1:
        x = [x_B[base_idx.index(i)] if i in base_idx else 0 for i in range(n)]
        # x = []
        # for i in range(n):
        #     if i in base_idx:
        #         x.append(x_B[i])
        #     else:
        #         x.append(0)
        
        print(f"Found optimal finite solution: {x}")
        break
    else:
        # print([x_B[k]/A[k, i] for k in range(m)])
        i = np.argmin([x_B[k]/A[k, j] for k in range(m)])# Am I sure there's no division by zero? - CHECK

        print(f"x_{j + 1} enters the base, x_{base_idx[i] + 1} exits the base")
        print(base_idx)
        base_idx[i] = j
        print(base_idx)

        theta = A[i, j]
        A = A / theta
        b = b / theta

    counter += 1
