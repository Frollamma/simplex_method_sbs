import numpy as np
# import sympy as sp

def is_tolerable(value, tolerance=10**(-7)):
    return (abs(value) <= tolerance).all()

def is_standard_form(A, b, c, A_rank = None):# IMPR
    # At thee moment I get input in the form of the triple (A, b, c), so I can perform few checks for now. In the future I'll get input in a different form (more similar to real problems) and I'll have to run more checks - IMPR
    # Checks if b has got all nonnegative elements
    # Checks if the rank of A is the biggest possible and there are no zero columns and rows
    no_zero_columns = np.all(np.any(A, axis=0))
    no_zero_rows = np.all(np.any(A, axis=1))

    # print(np.any(A, axis=0))
    # print(np.all(np.any(A, axis=0)))
    # print(np.any(A, axis=1))
    # print(np.all(np.any(A, axis=1)))

    if A_rank == None:
        A_rank = A.rank()

    # At the moment, I can't check if each element of b is nonnegative directly with sympy... - IMPR (I used .applyfunction but this kind of use is deprecated)
    # print(b)
    b = np.asarray(list(b))
    # print(b)
    # print(b >= 0)

    # print(A)
    # print(b)

    return A_rank == A.rows and no_zero_columns and no_zero_rows and (b >= 0).all()

#    return A_rank == A.rows and not no_zero_columns and not no_zero_rows and np.all(b >= 0)

def is_solution(A, b, x):
    return is_tolerable(np.dot(A, b) - x)

def is_feasible_solution(A, b, x):
    return (x >= 0).all() and is_solution(A, b, x)

# def is_basic_solution(A, b, x, tol=10**(-7)):
#     return is_solution(A, b, x) and True# TEMP! - CHECK L. 2 p. 41

# def is_basic_feasible_solution(A, b, x):
#     return is_solution(A, b, x) and (x >= 0).all() and



