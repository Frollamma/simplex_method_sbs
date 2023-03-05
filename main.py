import numpy as np

# import sympy as sp
from utils import *
from sympy.matrices import Matrix

# from sympy import Rational, pprint
# from fractions import Fraction

"""
Takes in input a linear programming problem in standard form
"""


A = input_matrix("Enter matrix A: ")  # Matrix of technical coefficents
b = input_matrix("Enter vector b: ")  # Right-hand sides
c = input_matrix(
    "Enter vector c: "
).transpose()  # Vector of costs (relative to the linear objective function)
method = input(
    """Choose a resolution method:
1) Complete (default)
2) FullTableau
3) TwoPhases

>> """
)
default_method = "Complete"

if method == "1":
    method = "Complete"
elif method == "2":
    method = "FullTableau"
elif method == "3":
    method = "TwoPhases"
elif method == "":
    method = default_method
else:
    raise ValueError("Unknown method")

# A = Matrix([
#     [0, 1, 4],
#     [-2, 1, 6]
# ])
# A = Matrix([
#     [0, 1, 4, 1, 0],
#     [-2, 1, 6, 0, 1]
# ])
# A = Matrix([
#     [1, 0, 0, 0, 1, 0, 0, 0],
#     [0, 1, 0, 0, 0, 1, 0, 0],
#     [2, 5, -1, 0, 0, 0, 1, 0],
#     [4, 2, 0, -1, 0, 0, 0, 1]
# ])
# A = Matrix([
#     [3, -2, 1, 0],
#     [1, 0, 0, 1]
# ])
# A = Matrix([[1, 2, 3/2], [4, 5, 6], [7, 23, 5]])

# b = Matrix([2, 2])
# b = Matrix([12, 5])
# b = Matrix([6, 4, 10, 8])

# c = Matrix([2, 3, 0]).transpose()
# c = Matrix([-1, -1, 0, 0, 0, 0, 0, 0]).transpose()
# c = Matrix([0, 0, 0, 0, 0, 0, 1, 1]).transpose()

# method = "FullTableau"  # TEMP

n = A.cols
m = A.rows

# This is useful for integer linear programming (but you have to add much more) - IMPR
# if is_unimodular_matrix(A):
#     print("Matrix A is unimodular!")

if method == "Complete":
    # This method is capable of choosing which of the other methods to use and when to use them
    pass
elif method == "FullTableau":
    [exit_code, v] = fulltableau_method(A, b, c, n, m)

    if exit_code == 1:
        print(f"Found optimal finite solution:")
        pprint(v)
    elif exit_code == 0:
        print(f"There's no finite optimal solution. The direction of improvement is")
        pprint(v)
    elif exit_code == -1:
        print(f"Reached max iterations. Last feasible basic solution is")
        pprint(v)

elif method == "TwoPhases":
    [exit_code, v] = twophases_method(A, b, c, n, m)

    if exit_code == 1:
        print(f"Found feasible basic solution for the original problem: {v}")
    elif exit_code == 0:
        print(f"There's no feasible basic solution for the original problem.")
    elif exit_code == -1:
        print(
            f"Reached max iterations. Last feasible basic solution for the auxiliary problem is {v}"
        )
else:
    raise ValueError(f"Method '{method}' not implemented")
