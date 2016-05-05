#!/usr/bin/python
import sys, os, re

import string_to_regex

with open(sys.argv[1]) as f:
    text = f.read()
skip = 1 if len(sys.argv) == 2 else int(sys.argv[2])
lines = text.splitlines()
regexes = set()

for line_index in range(0, len(lines), skip if skip else 1):
    if line_index % 100 == 0:
        print 'line_index: {}/{}'.format(line_index, len(lines))
    line = lines[line_index]

    if re.search('^(([0-9]{4}\-)|null )', line):
      split = line.split(' ', 1)
      _, after_timestamp = split
    else:
      after_timestamp = line

    regexes.add(string_to_regex.string_to_regex(after_timestamp))

with open(os.path.expanduser('~/Desktop/regexes.txt'), 'w') as f:
    f.write('\n'.join(regexes))
