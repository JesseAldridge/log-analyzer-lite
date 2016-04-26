#!/usr/bin/python
from __future__ import unicode_literals
import sys, codecs, re, shutil, os

import jellyfish


def cached_jaro(key_line, after_timestamp, mem={}):
  if not (key_line, after_timestamp) in mem:
    mem[key_line, after_timestamp] = jellyfish.jaro_distance(key_line, after_timestamp)
  return mem[key_line, after_timestamp]


def build_line_groups(lines, skip=None):
  line_groups = {}
  for line_index in range(0, len(lines), skip if skip else 1):
    if line_index % 100 == 0:
      sys.stderr.write('line_index: {}\n'.format(line_index))
      sys.stderr.write('line_groups: {}\n'.format(len(line_groups)))
    full_line = lines[line_index]
    full_line = full_line.strip('\n')
    if re.search('^(([0-9]{4}\-)|null )', full_line):
      split = full_line.split(' ', 1)
      _, after_timestamp = split
    else:
      after_timestamp = full_line
    for key_line in line_groups:
      if cached_jaro(key_line, after_timestamp) > .8:
        line_groups[key_line].append(after_timestamp)
        break
    else:
      line_groups[after_timestamp] = []
  return line_groups


if __name__ == '__main__':
  if len(sys.argv) == 1:
    line_groups = build_line_groups(['foo1', 'foo2', 'bar'])
    assert len(line_groups) == 2
  else:
    with open(sys.argv[1]) as f:
      text = f.read()
    lines = text.splitlines()
    skip = 1 if len(sys.argv) == 2 else int(sys.argv[2])
    line_groups = build_line_groups(lines, skip)

  if os.path.exists(os.path.expanduser('~/Desktop/line_groups')):
    shutil.rmtree(os.path.expanduser('~/Desktop/line_groups'))
  parent_dir = os.path.expanduser('~/Desktop/line_groups')
  os.mkdir(parent_dir)
  for i, t in enumerate(line_groups.iteritems()):
    key_line, matching_lines = t
    with open(os.path.join(parent_dir, str(i).zfill(3) + '.txt'), 'w') as f:
      f.write('\n'.join([key_line] + matching_lines))
