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
import time

def sol_error(x, true_x):
    return np.linalg.norm(true_x - x) / np.linalg.norm(true_x)

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
    if method == sla.spsolve:        # direct method
        start = time.clock()
        x = method(A, b)
        elapsed = time.clock() - start
        print("\t" + method.func_name + " solved " + 
            str(size) + " " + str(elapsed))

        #PROVO QUESTO METODO DIRETTO ULTERIORE
        start = time.clock()
        lu = sla.splu(A)
        x = lu.solve(b)
        elapsed = time.clock() - start
        print("\t" + "splu+solve" + " solved " + 
            str(size)+ " " + str(elapsed))


    else:                              # iterative methods
        # per accellerare la convergenza dei metodi iterativi
        # dobbiamo passare un precondizionatore (una matrice M,
        # che approssima l'inversa di A)
        # http://osdir.com/ml/python-scientific-user/2011-06/msg00249.html
        try:
            P = sla.spilu(A, drop_tol=1e-5)  
        except Exception as err:
            print("\t", err)
            print("\tPorta le tue sporche matrici singolari altrove...")
            return None, "NA"

        M = sla.LinearOperator(size, P.solve)

        # dobbiamo settare a mano la tolleranza in modo da avere
        # errore intorno a 1e-6
        toll = {
            'bicg':     1e-6,
            'bicgstab': 1e-15,
            'cg':       1e-6,
            'cgs':      1e-14,
            'gmres':    1e-18,
            'lgmres':   1e-12,
            'minres':   1e-13,
            'qmr':      1e-6
        }

        x, conv = method(A, b, tol=toll[str(method.func_name)], M=M)

        if conv == 0:
            print("\t" + method.func_name + " converged on " + 
                  str(size))

    return x, sol_error(x, true_x)

def main():
    A = csc_matrix(mmread('./matrici/mtx_files/non-simmetrica-23451.mtx'))
    print("> Done reading!")

    sol, err = solve_system(A, sla.bicgstab)
    print(">>  Soluzione: ", sol[0:3], " ...")
    print(">>  Errore: ", err)

if __name__ == "__main__":
    main()



