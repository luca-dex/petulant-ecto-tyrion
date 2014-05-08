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

import os
from scipy.io import mminfo, mmread 
                
## read sparse matrix from .mtx file
def read_matrix_scipy(filename):
    return mmread(filename)


def main():
    os.chdir('mtx_files')

    filename = "non-simmetrica-46902.mtx"

    print "Matrix is shaped like this:"
    print mminfo(filename)

    print "Now let's read the matrix!"
    m = read_matrix_scipy(filename)

    print "Done Reading"
    print "Matrix starts like this:"
    print m.data


if __name__ == '__main__':
    main()
