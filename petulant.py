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


def main():
    os.chdir("mtx_files")
        
    filename = "non-simmetrica-46902.mtx"

    print("Matrix is shaped like this:")
    print(mminfo(filename))

    print("\nNow let's read the matrix!")
    mat = mmread(filename)

    print("Done reading!")
    print("First entries:")
    print(mat.data)


if __name__ == '__main__':
    main()
