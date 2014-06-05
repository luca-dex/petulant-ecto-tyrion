#!/usr/bin/env python
# -*- coding: utf-8 -*-

# =======
# License
# =======
# 
# Rilasciato sotto lincenza maligna Unimiamib
# 
# Copyright (c) 2014, Alberto Donizetti, Luca De Sano, Massimiliano Scotti
# All rights reserved.
# See LICENSE.txt

from __future__ import print_function

import time

import numpy as np
from scipy.sparse import *
from scipy.io import mmread 
import scipy.sparse.linalg as sla 
import time

def sol_error(x, true_x):
    return np.linalg.norm(true_x - x) / np.linalg.norm(true_x)

current_x = None
def callback_func(xk):
    true_x = list(xrange(0, len(xk)))
    global current_x
    current_x = xk
    if sol_error(xk, true_x) < 1e-6:
        raise Exception("Finito!")


def solve_system(A, method):
    """
    Solve linear system Ax = b with A matrix in filename and
    b = (0, 1, 2, 3, ...) using the specified method
    """
    # find b vector such that Ax = b
    # with x = [0 1 2 ... size(m)]
    size = A.shape
    true_x = list(xrange(0, size[1]))
    b = A.dot(true_x)

    # solve Ax = b and check solution error
    # diretti
    if method in [sla.spsolve, direttolu]:
        x = method(A, b)
        print("\t" + method.func_name + " solved " + 
            str(size))
        return x, sol_error(x, true_x)

    # iterativi
    else:                             
        # per accellerare la convergenza dei metodi iterativi
        # dobbiamo passare un precondizionatore (una matrice M,
        # che approssima l'inversa di A)
        # http://osdir.com/ml/python-scientific-user/2011-06/msg00249.html
        try:
            P = sla.spilu(A, drop_tol=1e-5)  
        except Exception as err:
            print("\t", err)
            print("\tPorta le tue sporche matrici singolari altrove...")
            return None, "nan"

        M = sla.LinearOperator(size, P.solve)

        global current_x
        current_x = None
        try: 
            x, status = method(A, 
                               b, 
                               tol=1e-16, 
                               M=M,
                               maxiter=500,
                               callback=callback_func)
        except Exception:
            print("\t" + method.func_name + " converged on " +  str(size))
            return current_x, sol_error(current_x, true_x)

        if status != 0:
            print("\t" + method.func_name + " DIDN'T converge on " +
                  str(size) + " in less than 500 iterations")
            return current_x, sol_error(x, true_x)
        else:
            print("\t" + method.func_name + " converged on " +
                  str(size))
            return current_x, sol_error(x, true_x)

def direttolu(A, b):
    lu = sla.splu(A)
    x = lu.solve(b)
    return x

def test_altro_diretti(A, b):
    # Implement me :D
    return

def main():
    A = csc_matrix(mmread('./matrici/mtx_files/non-simmetrica-46902.mtx'))
    start = time.clock()
    P = sla.spilu(A, drop_tol=1e-5)
    M = sla.LinearOperator(A.shape, P.solve)
    sol, err = solve_system(A, sla.bicgstab)
    end = time.clock()

    true_x = list(xrange(0, 46902))
    print(">>  Soluzione (reale):", true_x[0], true_x[1], "...", 
          true_x[-2], true_x[-1])
    print(">>  Soluzione (approx): ", sol[0], sol[1], "...", 
          sol[-2], sol[-1])
    print(">>  Errore: ", err)
    print(">>  Tempo:", end - start, " secondi")

if __name__ == "__main__":
    main()



