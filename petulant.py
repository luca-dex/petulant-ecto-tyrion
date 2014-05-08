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

from scipy.sparse import *
from scipy import *

def read_matrix():
	f = open("simmetrica-46902.dat", "r")
	n, non_blank, form = f.readline().split()
	n = int(n)
	non_blank = int(non_blank)
	S = dok_matrix((n, n), dtype=float32)

	for line in f:
	    x, y, v = line.split()
	    x = int(x) - 1
	    y = int(y) - 1
	    v = float(v)
	    try:
	    	S[x, y] = v
	    except:
	    	print('x:', x, 'y: ', y, 'v: ', v)

	return S
	    	



def main():
	S = read_matrix()
	return S


if __name__ == '__main__':
	S = main()