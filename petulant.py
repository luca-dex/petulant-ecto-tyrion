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

def solve_system(filename, method, toll=1e-5):
    """
    Solve linear system Ax = b with A matrix in filename and
    b = (0, 1, 2, 3, ...) using the specified method
    """
    # read matrix from file and convert into csc_matrix format
    A = csc_matrix(mmread('../matrici/mtx_files/' + filename))
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




