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

import petulant
import time
import os, re
import scipy.sparse.linalg as sla

methods = (sla.spsolve,     # diretto
           sla.bicg,        # BIConjugate Gradient
           sla.bicgstab,    # BIConjugate Gradient Stabilized
           sla.cg,          # Conjugate Gradient
           sla.cgs,         # Conjugate Gradient Squared
           sla.gmres,       # Generalized Minimal Residual
           sla.lgmres,      # LGMRES 
           sla.minres,      # Minimal Residual
           sla.qmr,         # Quasi-minimal Residual
)

def solve_all(type, method):
    """
    test 1: risolve tutti i sistemi di tipo 'type' (symm o
    unsymm) usando il metodo specificato, ritorna i tempi
    di esecuzione e l'errore sulla soluzione
    """
    data = {}
    for filename in os.listdir('../matrici/mtx_files'):
        if type == "symm" and "non" in filename:
            continue
        if type == "unsymm" and "non" not in filename:
            continue
        start = time.clock()
        _, error = petulant.solve_system(filename, method)
        end = time.clock()
        key = re.search(r"(\d+)", filename).group(0)
        data[int(key)] = (end - start, error)
    return data


def test_1(type):
    os.chdir('./benchmarks results')
    with open('test1' + type + '.txt', 'w') as f:
        for method in methods:
            data = solve_all(type, method)
            times = [data[t][0] for t in sorted(data)]
            dimensions = sorted(data)
            f.write('%' + str(method) + '\n')
            f.write(str(dimensions) + '\n')
            f.write(str(times) + '\n')
            print(" " + str(method) + " done!")

def test_2(type):
    os.chdir('./benchmarks results')
    with open('test2' + type + '.txt', 'w') as f:
        for method in methods:
            data = solve_all(type, method)
            errors = [data[t][1] for t in sorted(data)]
            dimensions = sorted(data)
            f.write('%' + str(method) + '\n')
            f.write(str(dimensions) + '\n')
            f.write(str(errors) + '\n')
            print(" " + str(method) + " done!")

test_2("symm")



        



