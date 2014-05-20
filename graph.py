#!/usr/bin/env python
import numpy as np
import pylab as P
import os
import StringIO

# dimensioni delle matrici
x = None

# ogni riga dei file al posto giusto
salvati = {}

# chiavi di salvati
chiavi = []


# smacinamento cartelle coi risultati
for test in os.listdir('benchmarks_results'):
	with open('benchmarks_results/' + test) as t:
		a = t.readline()
		if x is None:
			a = a[1:-2].split(', ')
			x = np.array(list(map((lambda val: int(val)), a)))

		for row in t:
			if(row[0] is '%'):
				algorithm = row.split()[1]
			else:
				value = np.genfromtxt(StringIO.StringIO(row[1:-2]), delimiter=', ', dtype="float64")
				key = test + '_' + algorithm
				chiavi.append(key)
				salvati[key] = value

width = 0.2
base = np.arange(len(x))

#
# tempo di esecuzione
#

P.figure()

P.bar(base, salvati['test1simm times_spsolve'], width=width, color='b', label='simmetriche')
P.bar(base + width, salvati['test1unsymm times_spsolve'], width=width, color='r', label='non simmetriche')

P.legend(loc='best')

P.xlabel('Numero di elementi')
P.ylabel('Tempo (s)')
P.suptitle('Tempo con metodo diretto')
P.xticks(base + width, tuple(x))

#
# errore relativo
#

P.figure()
P.bar(base, salvati['test1simm errs_spsolve'], width=width, color='b', label='simmetriche')
P.bar(base + width, salvati['test1unsymm errs_spsolve'], width=width, color='r', label='non simmetriche')

P.legend(loc='best')
P.xlabel('Numero di elementi')
P.ylabel('Errore')
P.suptitle('Errore relativo con metodo diretto')
P.xticks(base + width, tuple(x))

#
# comparazione tempi matrici simmetriche
#

P.figure()
ax = P.gca()

miter = [v for v in chiavi if 'simm' in v and 'spsolve' not in v and 'times' in v]

for i in miter:
	title = i.split('_')[1]
	P.plot(base, salvati[i], label=title)

P.legend(loc='best')
ax.set_yscale('log')
P.xlabel('Numero di elementi')
P.ylabel('Tempo di esecuzione')
P.suptitle('Tempo di esecuzione per matrici simmetriche')
P.xticks(base + width, tuple(x))

#
# comparazione errori matrici simmetriche
#

P.figure()
ax = P.gca()

miter = [v for v in chiavi if 'simm' in v and 'spsolve' not in v and 'errs' in v]

for i in miter:
	title = i.split('_')[1]
	P.plot(base, salvati[i], label=title)

P.legend(loc='best')
ax.set_yscale('log')
P.xlabel('Numero di elementi')
P.ylabel('Errore')
P.suptitle('Errore per matrici simmetriche')
P.xticks(base + width, tuple(x))

#
# comparazione tempi matrici non simmetriche
#

P.figure()
ax = P.gca()

miter = [v for v in chiavi if 'unsymm' in v and 'spsolve' not in v and 'times' in v]

for i in miter:
	title = i.split('_')[1]
	P.plot(base, salvati[i], label=title)

P.legend(loc='best')
ax.set_yscale('log')
P.xlabel('Numero di elementi')
P.ylabel('Tempo di esecuzione')
P.suptitle('Tempo di esecuzione per matrici non simmetriche')
P.xticks(base + width, tuple(x))

#
# comparazione errori matrici non simmetriche
#

P.figure()
ax = P.gca()

miter = [v for v in chiavi if 'unsymm' in v and 'spsolve' not in v and 'errs' in v]

for i in miter:
	title = i.split('_')[1]
	P.plot(base, salvati[i], label=title)

P.legend(loc='best')
ax.set_yscale('log')
P.xlabel('Numero di elementi')
P.ylabel('Errore')
P.suptitle('Errore per matrici non simmetriche')
P.xticks(base + width, tuple(x))


#
# stampa tutto
#
P.show()

