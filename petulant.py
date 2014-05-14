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

import numpy as np
from scipy.sparse import *
from scipy.io import mmread 
import scipy.sparse.linalg as sla 

def sol_error(x, true_x):
    return np.linalg.norm(true_x - x) / np.linalg.norm(true_x)

def solve_system(A, method, toll=1e-6):
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
    if method == sla.spsolve:          # direct method
        x = method(A, b)
    else:                              # iterative methods
        # per accellerare la convergenza dei metodi iterativi
        # dobbiamo passare un precondizionatore (una matrice M,
        # che approssima l'inversa di A)
        # http://osdir.com/ml/python-scientific-user/2011-06/msg00249.html
        P = sla.spilu(A, drop_tol=1e-5)  
        print("> Computed Preconditioner P")
        M = sla.LinearOperator(size, P.solve)
        x, conv = method(A, b, tol=toll, M=M)
        if conv == 0:
            print("> method " + method.func_name + " converged.\n")


    return x, sol_error(x, true_x)

def main():
    A = csc_matrix(mmread('./matrici/mtx_files/simmetrica-46902.mtx'))
    print("> Done reading!")

    sol, err = solve_system(A, sla.lgmres, toll=1e-8)
    print(">>  Soluzione: ", sol[0:3], " ...")
    print(">>  Errore: ", err)

if __name__ == "__main__":
    main()



