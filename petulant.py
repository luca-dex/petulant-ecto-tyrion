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

import os
import numpy as np
from scipy.sparse import *
from scipy.io import mmread 
import scipy.sparse.linalg as sla 

def sol_error(x, true_x):
    return np.linalg.norm(true_x - x) / np.linalg.norm(true_x)

def solve_system(filename, method, toll=None):
    """
    read matrix from file and convert into csc_matrix format
    """
    A = csc_matrix(mmread(filename))
    size = A.shape

    # find b vector such that Ax = b
    # with x = [0 1 2 ... size(m)]
    true_x = [i for i in xrange(0, size[1])]
    b = A.dot(true_x)

    # solve Ax = b and check solution error
    if method == sla.spsolve:          # direct method
        x = method(A, b)
    else:                              # iterative methods
        # we need this because iterative methods 
        # return a tuple with (solution, info)
        x = method(A, b, tol=toll)[0]

    return x, sol_error(x, true_x)


def main():
    os.chdir("mtx_files")
    
    # solve unsymmetric system with a direct method
    sol1, err1 = solve_system('non-simmetrica-1891.mtx', sla.spsolve) 
    print("Sol: ", sol1)
    print("Err: ", err1)

    # solve simmetric system with an iterative method
    sol2, err2 = solve_system('simmetrica-1891.mtx', sla.bicg, toll=1e-4)
    print("Sol: ", sol2)
    print("Err: ", err2)


if __name__ == '__main__':
    main()
