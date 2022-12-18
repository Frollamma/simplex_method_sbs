import numpy as np
from sympy.logic.boolalg import Boolean
from sympy.matrices import Matrix, ones, zeros
from sympy import eye, pretty, pprint
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
    # In our case numerators are nonnegative (this is not important for the algorithm itself but it guarantees that if we get a result, it is positive)
    n = len(numerators)
    if n != len(denominators):
        raise ValueError("Iterables with different lenghts")
    
    i = 0
    while i < n and denominators[i] <= 0:
        i += 1
    
    if i == n:
        # This means that every denominator is nonpositive
        return -1

    current_min = numerators[i]/denominators[i]
    for k in range(i + 1, n):
        if denominators[i] != 0:
            possible_min = numerators[i]/denominators[i]
            if possible_min < current_min:
                i = k
                current_min = possible_min
    return i

# def is_integer_matrix(A: MutableDenseMatrix) -> Boolean:
#     if all([a.is_integer for a in list(A)]):
#         return True
#     return False

# def is_totally_unimodular_matrix(A: MutableDenseMatrix) -> bool:
#     m = min([A.rows, A.cols])
#     for submatrix_dim in range(1, m+1):
#         # We're considering a submatrix of submatrix_dim rows and submatrix_dim columns
#         for i in range(A.rows - submatrix_dim + 1):
#             for j in range(A.cols - submatrix_dim + 1):
#                 submatrix_det = A.row(range(i, i + submatrix_dim)).col(range(j, j + submatrix_dim)).det()
#                 if submatrix_det not in [-1, 0, 1]:
#                     return False
#     return True

# def is_unimodular_matrix(A: MutableDenseMatrix) -> bool:
#     m = min([A.rows, A.cols])
#     for k in range(m):
#         # We're considering a submatrix of m rows and m columns

#         # Now we have to find all the possible combinations of m indices (regardless of order)... - IMPR

#         for i in range(A.rows - m + 1):
#             for j in range(A.cols - m + 1):
#                 submatrix_det = A.row(range(i, i + m)).col(range(j, j + m)).det()
#                 if submatrix_det not in [-1, 0, 1]:
#                     return False
#     return True

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

# def is_basic_solution(A, b, x):
    # pass
# def is_basic_feasible_solution(A, b, x):
    # pass


# Simplex Method
def get_base_costs(c, base_indexes):
    return Matrix([c[i] for i in base_indexes]).transpose()

def compose_solution(x_B, base_indexes, n):
    '''n is solution lenght'''
    return Matrix([x_B[base_indexes.index(i)] if i in base_indexes else 0 for i in range(n)])# IMPR: it seems inefficient

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


## FullTableau Method
def fulltableau_method(A, b, c, n=None, m=None, base_indexes=None, max_iterations = 20):
    '''Returns a list [exit_code, v].
    exit_code can be 1, 0 or -1.
    If exit_code is 1, then a finite optimal solution has been found. v is the solution vector.
    If exit_code is 0, then we found out that there's no finite optimal solution. v is direction of improvement vector.
    if exit_code is -1, we did max_iterations iterations and didn't get any of the previous results. v is the last feasible basic solution we were working on.
    '''
    if n == None:
        n = A.cols
    if m == None:
        m = A.rows

    # Indexes of variable in the base at first iteration
    if base_indexes == None:
        base_indexes = input_indexes("Enter columns indexes of initial base matrix separated by comma: ")
    
    if not is_standard_form(A, b, c):
        raise ValueError("Problem not in standard form")

    if len(base_indexes) != m:
        raise ValueError(f"Number of base indexes doesn't match rank of technological coefficients matrix: {m}")


    # Starting base matrix
    B = A.col(base_indexes)

    if B.det() == 0:
        raise ValueError("Base matrix non invertible")

    # print_problem(A, b, c)        # IMPR: doesn't work
    print(f"In the base we have: {', '.join(get_variables_string_by_indexes(base_indexes))}")

    x = None
    counter = 0
    while counter < max_iterations:
        [x_B, z, rc, C] = compute_tableau(A, b, c, base_indexes)
        tableau = compose_tableau(x_B, z, rc, C)
        print_tableau(tableau)

        # j = np.where(np.asarray(rc) < 0)[0][0]
        j = first_negative_item_index(rc)
        # print(rc)
        # print(j)
        if j == -1: # All reduced costs are nonnegative
            x = compose_solution(x_B, base_indexes, n)
            return [1, x]
        else:
            l = argmin_of_positive_fractions(x_B, A[:, j])
            if l == -1:
                d = -A.col(j)
                return [0, d]

            print(f"{get_variable_string_by_index(j)} enters the base, {get_variable_string_by_index(base_indexes[l])} exits the base")
            #print(base_indexes)
            base_indexes[l] = j
            #print(base_indexes)

            theta = A[l, j]
            A = A / theta
            b = b / theta

        counter += 1

    return [-1, x]

## Two phases method
def twophases_method(A, b, c, n=None, m=None, base_indexes=None):
    # Phase 1
    if n == None:
        n = A.cols
    if m == None:
        m = A.rows

    # Indexes of variable in the base at first iteration
    if base_indexes == None:
        base_indexes = input_indexes("Enter columns indexes of initial base matrix separated by comma: ")
    base_indexes = zeros(1, m) # TEMP: I think I should not take base_indexes as argument...

    # I think I should not check that all the rows are independent, because I read that you might find a null row at some point and that's ok (I mean you can handle it) - CHECK - IMPR
    if not is_standard_form(A, b, c):
        raise ValueError("Problem not in standard form")

    if len(base_indexes) != m:
        raise ValueError(f"Number of base indexes doesn't match rank of technological coefficients matrix: {m}")


    print("Building auxiliary problem...")
    A_new = A.row_join(eye(m))
    c_new = zeros(1, n).row_join(ones(1, m))
    #print_problem(A_new, b, c_new)     # IMPR
    base_indexes = list(range(n, n + m))
    
    [exit_code, v] = fulltableau_method(A_new, b, c_new, n, m, base_indexes)

    # Phase 2
    if exit_code == 1:
        if v.is_zero:
            return [1, v.row(range(m))]     # Keep in mind that some auxiliary variables migth be still in base, you should handle it - IMPR
        else:
            return [0, v]
            
    elif exit_code == 0:
        # This should never happen (by theory)
        raise Exception("First Phase of Two Phases Method failed!")
    else:
        return [-1, v]


