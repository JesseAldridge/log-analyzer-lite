#!/usr/bin/python
import sys, os, re

import string_to_regex

path = sys.argv[1]
skip_num = int(sys.argv[2])
print 'reading...'
with open(path) as f:
    text = f.read()
print 'splitting...'
lines = text.splitlines()
print 'sampling...'
with open(os.path.expanduser('~/Desktop/sample.txt'), 'w') as f:
    for tick, line_index in enumerate(range(0, len(lines), skip_num)):
        if tick % 100 == 0:
            print '{:.2f}%'.format(100 * line_index / float(len(lines)))
        f.write(lines[line_index] + '\n')
