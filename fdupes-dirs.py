#!/usr/bin/env python3

# takes output of running fdupes
# and groups it into duplicate directories

import os
import sys

def main(argv):
    with open(argv[1], 'rb') as fin:
        fdupes = [i.split(b'\n') for i in fin.read().strip().split(b'\n\n')]
    dupes = {} # mapping from filename to canonical identifier
    curr_index = 0
    for i, files in enumerate(fdupes):
        for f in files:
            dupes[f] = curr_index + i

    d = {}
    for k, v in dupes.items():
        d[v] = sorted(d.get(v, []) + [k])
    with open(argv[2], 'wb') as fout:
        for g in sorted(d.values(), key=lambda i: i[0]):
            for i in g:
                fout.write(i)
                fout.write(b'\n')
            fout.write(b'\n')

if __name__ == '__main__':
    main(sys.argv)
