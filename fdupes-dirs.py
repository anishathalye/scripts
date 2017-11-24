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
    curr_index = len(dupes)

    file_list = fdupes
    passnum = 0
    while file_list:
        print('PASS %d' % passnum)
        passnum += 1
        dup_dirs = get_dup_dirs(file_list, dupes)
        for i, dirs in enumerate(dup_dirs):
            for d in dirs:
                dupes[d] = curr_index + i
        curr_index = len(dupes)
        file_list = dup_dirs

    # now how do we print this? we can print out the dupes map, skipping
    # anything for which there is a more general description
    dupes_filtered = {}
    for f in dupes:
        if os.path.dirname(f) not in dupes:
            dupes_filtered[f] = dupes[f]
    pl = sorted((v, k) for k, v in dupes_filtered.items())
    prev_v = 0
    with open(argv[2], 'wb') as fout:
        for i in pl:
            if prev_v != i[0]:
                fout.write(b'\n')
                prev_v = i[0]
            fout.write(i[1])
            fout.write(b'\n')

def get_dup_dirs(file_list, dupes):
    dup_dirs = {} # mapping from lexicographically first -> set of matching dirs
    checked = set()
    print('checking %d files' % len(file_list))
    for index, files in enumerate(file_list):
        if (index+1) % 1000 == 0:
            print('checking %d of %d' % (index+1, len(file_list)))
        dirs = [os.path.dirname(f) for f in files]
        for i in range(len(dirs)):
            for j in range(i+1, len(dirs)):
                d1, d2 = dirs[i], dirs[j]
                if d1 == d2:
                    continue
                if not (d1, d2) in checked:
                    checked.add((d1, d2))
                    if dirs_identical(d1, d2, dupes):
                        # add to dup_dirs
                        if d1 > d2:
                            d1, d2, = d2, d1
                        assert d1 < d2
                        if d1 in dup_dirs:
                            dup_dirs[d1].add(d2)
                        elif d2 in dup_dirs:
                            dup_dirs[d1] = dup_dirs[d2]
                            dup_dirs[d1].add(d2)
                            del dup_dirs[d2]
                        else:
                            dup_dirs[d1] = {d2}
    dup_dirs = [[k] + list(v) for k, v in dup_dirs.items()] # same format as file_list
    return dup_dirs

# dupes is mapping from filename to canonical identifier
def dirs_identical(d1, d2, dupes):
    f1 = sorted(os.listdir(d1))
    f2 = sorted(os.listdir(d2))
    if f1 != f2:
        return False
    for f in f1:
        f1_full = os.path.join(d1, f)
        f2_full = os.path.join(d2, f)
        if f1_full not in dupes or f2_full not in dupes or dupes[f1_full] != dupes[f2_full]:
            return False
    return True

if __name__ == '__main__':
    main(sys.argv)
