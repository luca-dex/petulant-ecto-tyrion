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

## eseguimi dalla cartella contenente i file .dat scaricati 
## da matapp per convertirli in formato .mtx

import os

def change_format(filename):
    """
    create a .mtx file from a .dat file (filename) so we can
    read matrices with the scipy builtin sparse matrix reader 
    """
    with open(filename) as f:
    
        comment = "%%MatrixMarket matrix coordinate real "
        if "non" in f.name:
            comment += "general\n"
        else:
            comment += "symmetric\n"
            
        n, l, form = f.readline().split()
        form = n + " " + n + " " + l + "\n"
          
        filename_new = "mtx_files/" + filename.replace("dat", "mtx")
        
        with open(filename_new, "w") as f_new:
            
            f_new.write(comment)
            f_new.write(form)
            for line in f:
                f_new.write(line)


def main():
    """
    change to Matrix Market Format all files in the current dir
    """
    if os.path.exists("mtx_files"):
        print("Directory \'mtx_files\' found. Nothing to do here...")
        return
    
    # else we create the folder and convert all the .dat files
    os.mkdir("mtx_files")
        
    for filename in os.listdir('.'):
        if "dat" in filename:
            change_format(filename)


if __name__ == '__main__':
    main()

