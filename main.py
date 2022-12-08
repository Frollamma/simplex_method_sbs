import numpy as np
#import sympy as sp
from utils import *
from sympy.matrices import Matrix
# from sympy import Rational, pprint
# from fractions import Fraction

'''
Takes in input a linear programming problem in standard form
'''


# Matrix of technical coefficents
A = Matrix([
    [1, 0, 0, 0, 1, 0, 0, 0],
    [0, 1, 0, 0, 0, 1, 0, 0],
    [2, 5, -1, 0, 0, 0, 1, 0],
    [4, 2, 0, -1, 0, 0, 0, 1]
])
# A = Matrix([
#     [3, -2, 1, 0],
#     [1, 0, 0, 1]
# ])
# A = Matrix([[1, 2, Rational(3, 2)], [4, 5, 6], [7, 23, 5]])

# Right-hand sides
# b = Matrix([12, 5])
b = Matrix([6, 4, 10, 8])

# Vector of costs (relative to the linear objective function)
#c = Matrix([-1, -1, 0, 0, 0, 0, 0, 0]).transpose()
c = Matrix([0, 0, 0, 0, 0, 0, 1, 1]).transpose()

# Indexes of A columns corresponding to the base
base_idx = [4, 5, 6, 7]

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
    # print(rc)
    print(j)
    if j == -1:
        x = [x_B[base_idx.index(i)] if i in base_idx else 0 for i in range(n)]# IMPR: it seems inefficient
        print(f"Found optimal finite solution: {x}")
        break
    else:
        # print([x_B[k]/A[k, j] for k in range(m)])
        # print([x_B[k]/A[k, j] for k in range(m) if A[k, j] != 0])
        # # i = np.argmin([x_B[k]/A[k, j] for k in range(m) if A[k, j] != 0])     # This is not the solution because gets the wrong index
        # i = np.argmin([x_B[k]/A[k, j] for k in range(m)])# Division by zero can happen and cause problems... - CHECK

        i = argmin_of_fractions(x_B, A[:, j])
        if i == -1:         # This should never happen
            raise Exception("Found null column")

        print(f"x_{j + 1} enters the base, x_{base_idx[i] + 1} exits the base")
        print(base_idx)
        base_idx[i] = j
        print(base_idx)

        theta = A[i, j]
        A = A / theta
        b = b / theta

    counter += 1
