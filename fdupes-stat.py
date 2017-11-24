#!/usr/bin/env python3

# takes output of running fdupes
# and groups it into duplicate directories

import os
import sys

def main(argv):
    with open(argv[1], 'rb') as fin:
        fdupes = [i.split(b'\n') for i in fin.read().strip().split(b'\n\n')]

    files_by_size = []
    required = used = 0
    for group in fdupes:
        sz = os.path.getsize(group[0])
        required += sz
        used += sz*len(group)
        for f in group:
            files_by_size.append((sz, f))
    print('required: %d' % required)
    print('used: %d' % used)
    print('')
    for e in sorted(files_by_size):
        print(e)

if __name__ == '__main__':
    main(sys.argv)
