#!/usr/bin/python
import sys, re, string, itertools, colorsys

# Read a list of regexes, assign them colors, and map them to input lines.

with open(sys.argv[1]) as f:
  regexes = f.read().splitlines()

def rgb_to_hex(rgb):
  return '#%02x%02x%02x' % rgb

regexes.sort(key=lambda s: -len(s))
HSV_tuples = [(x * 1.0 / len(regexes), 0.5, 1.0) for x in range(len(regexes))]
RGB_tuples = [tuple((x * 255) for x in colorsys.hsv_to_rgb(*t)) for t in HSV_tuples]
hex_colors = {regex: rgb_to_hex(rgb) for regex, rgb in zip(regexes, RGB_tuples)}
css_names = list(''.join(x) for x in itertools.product(string.lowercase, string.lowercase))


print '<style>'
for css_name, color in zip(css_names, hex_colors.values()):
  print '.{} {{ background-color: {} }}'.format(css_name, color)
print '</style>'

sys.stderr.write('num regexes: {}\n'.format(len(regexes)))
for line_num, line in enumerate(sys.stdin):
  line = line.strip('\n')
  for i, regex in enumerate(regexes):
    if re.search(regex, line):
      print '<div class="{}">{}</div>'.format(css_names[i], line)
      break
  else:
    if line_num % 100 == 0:
      print '<div class="{}">{}</div>'.format(css_names[-1], line)
