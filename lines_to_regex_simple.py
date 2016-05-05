#!/usr/bin/python
import sys, os, re

import string_to_regex

skip = 1 if len(sys.argv) == 1 else int(sys.argv[1])
with open(os.path.expanduser('~/Desktop/norm.txt')) as f:
    text = f.read()
lines = text.splitlines()
regexes = set()

for line_index in range(0, len(lines), skip if skip else 1):
    print '{:.2f}%'.format(100 * line_index / float(len(lines)))
    line = lines[line_index]
    _, after_timestamp = line.split(' ', 1)
    regexes.add(string_to_regex.string_to_regex(after_timestamp))

with open(os.path.expanduser('~/Desktop/regexes.txt'), 'w') as f:
    f.write('\n'.join(regexes))
