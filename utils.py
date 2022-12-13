import numpy as np
from sympy.matrices import Matrix
from sympy import pretty, pprint
from sympy.parsing.sympy_parser import parse_expr
from sympy.matrices.dense import MutableDenseMatrix


# Generic
## Math
def first_negative_item_index(my_list):
    for i in range(len(my_list)):
        if my_list[i] < 0:
            return i
    return -1

def argmin_of_positive_fractions(numerators, denominators):
    # In our case numerators are nonnegative
    n = len(numerators)
    if n != len(denominators):
        raise ValueError("Iterables with different lenghts")
    
    i = 0
    while i < n and denominators[i] <= 0:
        i += 1
    
    if i == n:
        # This means that every denominator is 0
        return -1

    current_min = numerators[i]/denominators[i]
    for k in range(i + 1, n):
        if denominators[i] != 0:
            possible_min = numerators[i]/denominators[i]
            if possible_min < current_min:
                i = k
                current_min = possible_min
    return i
                
## Parsing
def input_sympy(prompt=''):
    return parse_expr(input(prompt))

def input_matrix(prompt='') -> MutableDenseMatrix:
    matrix = parse_expr(f"Matrix({input(prompt)})")
    if type(matrix) == MutableDenseMatrix:
        return matrix
    else:
        raise ValueError("Input is not a Matrix")

def input_indexes(prompt='') -> list[int]:
        text = input(prompt)
        indexes = text.strip('[]').replace(' ', '').split(',')
        return [int(i)-1 for i in indexes]

def is_degenerate(x, n, base_indexes):
    # all([x(i) == 0 for i in base_indexes])

    exists_zero_outside_base = False
    i = 0
    while i < n:
        if i in base_indexes:
            if x(i) == 0:
                exists_zero_outside_base = True
        else:
            # All x(i) should > 0, if there's a x(i) = 0, we return False
            if x(i) == 0:
                return False

    return exists_zero_outside_base

def get_variable_string_by_index(index):
    return f'x_{index+1}'

def get_variables_string_by_indexes(indexes):
    return [get_variable_string_by_index(i) for i in indexes]

## Printing
def print_problem(A, b, c, mode='plain'):
    '''Mode can be \'plain\' or \'latex\''''
    print("We want to solve")
    print(pretty(A), "x", "=", pretty(b)) # Doesn't display properly


def print_tableau(tableau, mode='plain'):
    '''Mode can be \'plain\' or \'latex\''''
    if mode=='plain':
        pprint(tableau)
    elif mode=='LaTeX':# TEMP - IMPR
        pass


## Numerical approximation (I think I'll delete this...)
# def is_tolerable(value, tolerance=10**(-7)):
#     return (abs(value) <= tolerance).all()

# def is_solution_approx(A, b, x):
#     return is_tolerable(np.dot(A, x) - b)

# def is_feasible_solution_approx(A, b, x):
#     return (x >= 0).all() and is_solution_approx(A, b, x)

# def is_basic_solution_approx(A, b, x, tol=10**(-7)):
#     return is_solution_approx(A, b, x) and True# TEMP! - CHECK L. 2 p. 41


# Linear Programming Problem theory
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
    b = np.asarray(list(b))# IMPR
    # print(b)
    # print(b >= 0)

    # print(A)
    # print(b)

    return A_rank == A.rows and no_zero_columns and no_zero_rows and (b >= 0).all()


def is_solution(A, b, x):
    '''Checks if x is the solution to the linear system Ax = b'''
    return A*x == b

def is_feasible_solution(A, b, x):
    return (np.asarray(list(x)) >= 0).all() and is_solution(A, b, x) # IMPR

# def is_basic_solution_approx(A, b, x):
    # pass
# def is_basic_feasible_solution(A, b, x):
    # pass


# Full tableau Method
def get_base_costs(c, base_indexes):
    return Matrix([c[i] for i in base_indexes]).transpose()

def compute_tableau(A, b, c, base_indexes):
    B = A[:, base_indexes]
    invB = B.inv()
    x_B = invB * b
    c_B = get_base_costs(c, base_indexes)
    C = invB * A
    rc = c - c_B * invB * A # Reduced costs
    z = - c_B * x_B
    
    return [x_B, z, rc, C]
    
def compose_tableau(x_B, z, reduced_costs, C):
    row = z.row_join(reduced_costs)
    tableau = x_B.row_join(C)
    tableau = row.col_join(tableau)
    
    return tableau




