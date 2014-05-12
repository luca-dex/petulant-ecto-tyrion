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

def solve_all(type, method):
    """
    test 1: risolve tutti i sistemi di tipo 'type' (simmetrici o
    non simmetrici) usando il metodo specificato, ritorna i tempi
    di esecuzione e l'errore sulla soluzione
    """
    data = {}
    for filename in os.listdir('./mtx_files'):
        if type not in filename:
            continue
        start = time.clock()
        _, error = petulant.solve_system('mtx_files/' + filename, method)
        end = time.clock()
        key = re.search(r"(\d+)", filename).group(0)
        data[key] = (end - start, error)
    return data

data = solve_all("non", sla.spsolve)

for k, v in data.items():
    print(k, ": time = ", v[0], ", err =  ", v[1])
        



