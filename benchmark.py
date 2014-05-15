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
import time, os, re
from scipy.sparse import *
from scipy.io import mmread
import scipy.sparse.linalg as sla

methods = (sla.spsolve,     # diretto
           # sla.bicg,        # BIConjugate Gradient
           sla.bicgstab,    # BIConjugate Gradient Stabilized
           # sla.cg,          # Conjugate Gradient
           sla.cgs,         # Conjugate Gradient Squared
           sla.gmres,       # Generalized Minimal Residual
           sla.lgmres,      # LGMRES 
           # sla.minres,      # Minimal Residual
           # sla.qmr,         # Quasi-minimal Residual

           # bicg non supporta precondizionatore via LinearOperator
           # minres non converge alla soluzione 
           # qmr necessita di 2 precondizionatori
)

symm = {}
unsymm = {}

def read_matrices():
    os.chdir('./matrici/mtx_files')
    for mtx_file in os.listdir('.'):
        dim = int(re.search(r"(\d+)", mtx_file).group(0))
        A = csc_matrix(mmread(mtx_file))
        if 'non' in mtx_file:
            unsymm[dim] = A
        else:
            symm[dim] = A
    os.chdir('../../benchmarks_results')

def solve_all(type, method):
    """
    Risolve tutti i sistemi di tipo 'type' (symm o
    unsymm) usando il metodo specificato, ritorna i tempi
    di esecuzione e l'errore sulla soluzione
    """
    data = {}
    Matrices = symm if type == 'symm' else unsymm
    for dim in sorted(Matrices):
        A = Matrices[dim]
        start = time.clock()
        sol, error = petulant.solve_system(A, method)
        print("\t error:", error)
        end = time.clock()
        data[dim] = (end - start, error)
    return data


def test_1(type):
    """
    Tutti i sistemi di un certo tipo 'type' (symm o 
    unsymm) usando tutti i metodi. Genera due files
    (times and errs) rispettivamente con i tempi di 
    esecuzione e gli errori commessi
    """
    f_times = open('test1' + type + ' times', 'w')
    f_errs = open('test1' + type + ' errs', 'w')
    
    write_dims = True
    for method in methods:
        print("> starting " + str(method))

        # risolve tutti i sistemi ed estra i dati dal dict
        data = solve_all(type, method)
        dims = sorted(data)
        times = [data[t][0] for t in dims]
        errs = [data[t][1] for t in dims]

        # scrive su file gli array
        if write_dims:
            f_times.write(str(dims) + '\n')
            f_errs.write(str(dims) + '\n')
            write_dims = False

        f_times.write('%' + str(method) + '\n')
        f_errs.write('%' + str(method) + '\n')
        f_times.write(str(times) + '\n')
        f_errs.write(str(errs) + '\n')
        print("\n\n")

    f_times.close()
    f_errs.close()


read_matrices()
print('> done reading!\n')

test_1('simm')
print("\n\n***** Unsymmetric Matrices *****\n")

test_1('unsymm')        



