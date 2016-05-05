#!/usr/bin/python
import sys, os, select, re
from datetime import datetime

'''
Split the timestamp prefix out of the passed line if it exists.
'''

class g:
  time_regex = None


def normalize_timestamp(line, should_fast_chop=False):
  # 2016-04-25T01:13:17.425 foo bar -> (dt, "foo bar")

  if should_fast_chop:
    # 01234567890123456789012
    # 2013-04-12T15:40:53.306

    bounds = (
      ((0, 4), (5, 7), (8, 10), (11, 13), (14, 16), (17, 19)) +
      (((20, 23),) if len(line) >= 23 else ()))
    slices = [
      line[start:end] for start, end in bounds
      if end <= len(line) and line[start:end].isdigit()]
    if len(slices) < 6:
      return (None, line)
    remainder = line[bounds[-1][-1] + 1:]
    return (
      "{}-{}-{}T{}:{}:{}{}".format(*(
        slices[:6] + ['.' + slices[6] if len(slices) > 6 else ''])),
      remainder)

  if not g.time_regex:
    for regex in [
      # 2016  - 03   -  04  T  20  :  18  :  29   .310762   +   00   : 00
      r'[0-9]+-[0-9]+-[0-9]+T[0-9]+:[0-9]+:[0-9]+\.[0-9]+(\+|\-)[0-9]+:[0-9]+',
      # 2016  - 04   -  25  T  01  :  13  :  17   . 425     -   0700
      r'[0-9]+-[0-9]+-[0-9]+T[0-9]+:[0-9]+:[0-9]+\.[0-9]+(\+|\-)[0-9]+']:
      match = re.search(regex, line)
      if match:
        g.time_regex = regex
        break
  match = None
  if g.time_regex:
    match = re.search(g.time_regex, line)
  return (match.group(), re.sub(g.time_regex, '', line).strip()) if match else (None, line)


def test_list(pairs, should_fast_chop):
  for in_str, expected in pairs:
    g.time_regex = None
    split = normalize_timestamp(in_str, should_fast_chop=should_fast_chop)
    print 'in_str:', in_str
    print ' split:', split
    print
    assert split == expected

def test():

  test_list([
    #  line                              # expected split
    ('2012-06-24 22:40:02', ('2012-06-24T22:40:02', '')),
    ('2013-05-24 09:11:02,346 INFO', ('2013-05-24T09:11:02.346', 'INFO')),
    ('2013-04-12T15:40:53.306 [ZEP_TRIGGER_PLUGIN_SPOOL]',
      ('2013-04-12T15:40:53.306', '[ZEP_TRIGGER_PLUGIN_SPOOL]')),
    ('foo', (None, 'foo')),
    ('', (None, '')),
    ('    ', (None, '    ')),
    ('Traceback (most recent call last)', (None, 'Traceback (most recent call last)'))
    ], should_fast_chop=True)

  test_list([
    ('129 <190>1 2016-03-04T20:18:29.310762+00:00 app web.10 - - SQLALCHEMY_TEST_DATABASE_URI: None',
        ('2016-03-04T20:18:29.310762+00:00',
          '129 <190>1  app web.10 - - SQLALCHEMY_TEST_DATABASE_URI: None')),
    ('2016-04-25T01:13:32.444-0700', ('2016-04-25T01:13:32.444-0700', '')),
    ], should_fast_chop=False)

def main(path=None):
  print 'reading...'
  with open(path) as f:
    text = f.read()
  print 'splitting...'
  lines = text.splitlines()
  print 'processing...'
  with open(os.path.expanduser('~/Desktop/norm.txt'), 'w') as f:
    for i, line in enumerate(lines):
      if i % 10000 == 0:
        print '{:.2f}%'.format(100 * i / float(len(lines)))
      dt_str, after_timestamp = normalize_timestamp(line)
      f.write(' '.join((dt_str or 'null', after_timestamp.rstrip('\n'))) + '\n')

if __name__ == '__main__':
  if len(sys.argv) == 1:
    test()
  else:
    main(sys.argv[1])
