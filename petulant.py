#!/usr/bin/env python
# -*- coding: utf-8 -*-

# =======
# License
# =======
# 
# Rilasciato sotto lincenza maligna Unimiamib
# 
# 
# Copyright (c) 2014, Alberto Donizetti, Luca De Sano, Massimiliano Scotti
# All rights reserved.
# See LICENSE.txt

import os
from scipy.io import mminfo, mmread 

def change_format(filename):
    """
    change .dat file to Matrix Market Format
    """
    with open(filename) as f:
    
        comment = "%%MatrixMarket matrix coordinate real "
        if "non" in f.name:
            comment += "unsymmetric\n"
        else:
            comment += "symmetric\n"
            
        n, l, form = f.readline().split()
        form = "" + n + " " + n + " " + l + "\n"
          
        filename_new = "mtx_files/" + filename.replace("dat", "mtx")

        with open(filename_new, "w") as f_new:
            
            f_new.write(comment)
            f_new.write(form)
            for line in f:
                f_new.write(line)


def change_all():
    """
    change to Matrix Market Format all files in the current dir
    """
    if not os.path.exists("mtx_files"):
        os.mkdir("mtx_files")
        
    for filename in os.listdir('.'):
        if "dat" in filename:
            change_format(filename)
                
## read sparse matrix in .mtx file
def read_matrix_scipy(filename):
    return mmread(filename)


def main():
    # run me if you don't have the .mtx files
    change_all() 

    os.chdir("mtx_files")
        
    filename = "simmetrica-46902.mtx"

    print("Matrix is shaped like this:")
    print(mminfo(filename))

    print("\nNow let's read the matrix:")
    print(read_matrix_scipy(filename).data)


if __name__ == '__main__':
    main()
