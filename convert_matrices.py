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

## create a .mtx file from a .dat file (filename) so we can
## read matrices with the scipy builtin sparse matrix reader 
def change_format(filename):
    f = open(filename)
    
    comment = "%%MatrixMarket matrix coordinate real "
    if "non" in f.name:
        comment += "unsymmetric\n"
    else:
        comment += "symmetric\n"
        
    n, l, form = f.readline().split()
    form =  n + " " + n + " " + l + "\n"
        
    f_new = open("mtx_files/" + filename.replace("dat", "mtx"), "w")
        
    f_new.write(comment)
    f_new.write(form)
    for line in f.readlines():
        f_new.write(line)
                
    f.close()
    f_new.close()


## change the format of all the .dat files in the current
## directory. Put the .mtx files in a new folder name mtx_files
def change_all():
    # if a 'mtx_files' folder exists in curr dir, we just return
    if os.path.exists("mtx_files"):
        return
    
    # else we create the folder and convert all the .dat files
    os.mkdir("mtx_files")
        
    for filename in os.listdir('.'):
        if "dat" in filename:
            change_format(filename)

change_all()

