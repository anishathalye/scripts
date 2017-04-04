#!/usr/bin/env python3

import subprocess
import argparse
import sys
import os

def multiline(s):
    return '\n'.join(l.lstrip() for l in s.split('\n')).strip()

def fetch_key(fingerprint, keyserver):
    with open(os.devnull) as devnull:
        subprocess.check_call([
            'gpg',
            '--keyserver',
            keyserver,
            '--recv-key',
            fingerprint
        ], stdout=devnull, stderr=devnull)

def key_info(fingerprint):
    with open(os.devnull) as devnull:
        output = subprocess.check_output([
            'gpg',
            '--fingerprint',
            '-k',
            fingerprint
        ], stderr=devnull).decode('utf8')
    res = {'uid': []}
    for line in output.split('\n'):
        if line.startswith('      Key fingerprint ='):
            res['fingerprint'] = line.split('=', 1)[1].strip()
        if line.startswith('uid'):
            uid = line.split(']', 1)[1].strip()
            res['uid'].append(uid)
    return res

def format_single(res):
    template = multiline('''
    \\begin{element}
    \\begin{minipage}{\\linewidth}
    \\begin{verbatim}
    %s
    \\end{verbatim}
    \\end{minipage}
    \\end{element}
    ''')
    uids = '\n'.join('  UID: %s' % i for i in res['uid'])
    body = 'Fingerprint: %s\n%s' % (res['fingerprint'], uids)
    return template % body

def make_document(data, copies):
    template = multiline('''
    \\documentclass[11pt,letterpaper]{article}
    \\usepackage[letterpaper, margin=1in]{geometry}
    \\newenvironment{element}{
        \\par
        \\cleaders\\vbox to 2\\baselineskip{
          \\vss
          \\hrule width\\linewidth
          \\vss
        }\\vskip2\\baselineskip
    }{}
    \\pagenumbering{gobble}
    \\begin{document}
    %s
    \\end{document}
    ''')
    parts = []
    for res in data:
        for _ in range(copies):
            parts.append(format_single(res))
        parts.append('\\clearpage')
    body = '\n'.join(parts)
    return template % body

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True, help='fingerprints, one per line')
    parser.add_argument('-c', '--copies', default=1, type=int, help='number of copies per fingerprint')
    parser.add_argument('-k', '--keyserver', default='hkps://pgp.mit.edu', help='keyserver')
    parser.add_argument('-o', '--output', help='output file')
    options = parser.parse_args()

    data = []
    with open(options.input) as fin:
        for line in fin:
            fpr = line.strip()
            if fpr:
                try:
                    info = key_info(fpr)
                except subprocess.CalledProcessError:
                    fetch_key(fpr, options.keyserver)
                    info = key_info(fpr)
                data.append(info)

    output = make_document(data, options.copies)

    if options.output:
        with open(options.output, 'w') as fout:
            fout.write(output)
    else:
        print(output)

if __name__ == '__main__':
    main()
