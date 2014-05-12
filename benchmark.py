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

def dump_data_to_file(data, filename):
    print(data)
    with open(filename, "w") as f:
        times = [data[t][0] for t in sorted(data)]
        errors = [data[t][1] for t in sorted(data)]
        f.write(str(times))
        f.write('\n')
        f.write(str(errors))

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
        data[int(key)] = (end - start, error)
    return data

data = solve_all("non", sla.spsolve)
dump_data_to_file(data, "non-simmetriche.data")


        



