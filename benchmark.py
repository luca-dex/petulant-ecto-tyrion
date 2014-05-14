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
           sla.cg,              # Conjugate Gradient
           sla.cgs,             # Conjugate Gradient Squared
           sla.gmres,           # Generalized Minimal Residual
           sla.lgmres,          # LGMRES 
           sla.minres,          # Minimal Residual
           sla.qmr,             # Quasi-minimal Residual
)

def solve_all(type, method):
    """
    test 1: risolve tutti i sistemi di tipo 'type' (symm o
    unsymm) usando il metodo specificato, ritorna i tempi
    di esecuzione e l'errore sulla soluzione
    """
    data = {}
    for filename in os.listdir('.'):
        if type == "symm" and  "non" in filename:
            continue
        if type == "unsymm" and "non" not in filename:
            continue
        start = time.clock()
        _, error = petulant.solve_system(filename, method)
        end = time.clock()
        key = re.search(r"(\d+)", filename).group(0)
        data[int(key)] = (end - start, error)
    return data

os.chdir('./matrici/mtx_files')

data = solve_all("symm", sla.spsolve)
petulant.dump_data_to_file(data, 'result.txt')


        



