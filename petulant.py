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
    if method in [sla.spsolve, diretto_lu]:
        x = method(A, b)
        print("\t" + method.func_name + " solved " + 
            str(size))

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



def diretto_lu(A, b):
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



