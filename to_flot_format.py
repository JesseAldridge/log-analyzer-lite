#!/usr/bin/python
import sys, json, re, time, os, shutil
from datetime import timedelta
from dateutil import parser

'''
Read list of regexes from the passed file.
Read piped in timestamped lines.
For each line, add the line to the matching layer.
Dump the layers to an html file that will use flot to render the graph.
 ___
|foo|___
|___|foo|
|bar|___|
|   |bar|
|___|___|
0   1   2

layer_map = {
  "foo_regex": {
    dt1: ["match 1", "match 2", ...],
    dt2: ["match 1", "match 2", ...]
  },
  "bar_regex": {
    dt1: [...],
    ...
  },
  ...
}

flot_data = [
  {label: 'foo regex', data:[[dt1, count], [dt2, count], ...]},
  {label: 'bar regex', data:[[dt1, count], [dt2, count], ...]},
]
'''

with open(sys.argv[1]) as f:
  regexes = f.read().splitlines()

with open(sys.argv[2]) as f:
  lines = f.read().splitlines()

regex_to_time = {}

# Map each regex to lists of matching lines grouped by hour.
layer_map = {}
all_regex_matches = {}
min_hour_str, max_hour_str = None, None
dt_str = None
skip = int(sys.argv[3]) if len(sys.argv) == 4 else 1
for i in range(0, len(lines), skip):
  if i % 100 == 0:
    print '{:<4}/{:<4}'.format(i, len(lines))
  line = lines[i]
  line = line.strip('\n')
  prev_dt_str = dt_str
  dt_str, after_timestamp = line.split(' ', 1)
  after_timestamp = after_timestamp.strip()
  if dt_str == "null":
    dt_hourly_str = None if prev_dt_str is None else prev_dt_str
  else:
    dt_hourly_str = dt_str.split(':', 1)[0] + ':00:00'
    if min_hour_str is None or dt_hourly_str < min_hour_str:
      min_hour_str = dt_hourly_str
    if max_hour_str is None or dt_hourly_str > max_hour_str:
      max_hour_str = dt_hourly_str
  for regex in sorted(regexes, key=lambda s: -len(s)):
    start_time = time.time()
    match = re.match(regex, after_timestamp)
    end_time = time.time()
    regex_to_time.setdefault(regex, 0)
    regex_to_time[regex] += end_time - start_time
    if match:
      layer_map.setdefault(regex, {})
      layer_map[regex].setdefault(dt_hourly_str, [])
      layer_map[regex][dt_hourly_str].append(after_timestamp)
      all_regex_matches.setdefault(regex, [])
      all_regex_matches[regex].append(after_timestamp)
      break
  else:
    # TODO: every line should be matched
    print 'unmatched:', after_timestamp


# Build hourly range of datetimes.  Handle initial null timestamps.
hourly_dts = [None]
min_dt = parser.parse(min_hour_str)
max_dt = parser.parse(max_hour_str)
dt = min_dt
while dt <= max_dt:
  hourly_dts.append(dt)
  dt += timedelta(hours=1)

# Translate the layer map into flot format.
flot_layers = []
for regex, line_groups in layer_map.iteritems():
  layer = {'label': regex, 'data': []}
  flot_layers.append(layer)
  for dt in hourly_dts:
    dt_str = 'null' if dt is None else dt.isoformat()
    layer['data'].append([dt_str, len(line_groups[dt_str]) if dt_str in line_groups else 0])

# Read html template, and write out
template_path = 'stuff/stack_template.html'
static_dir = 'static/'

with open(template_path) as f:
  template_str = f.read()
flot_layers.sort(key=lambda layer: -len(all_regex_matches[layer['label']]))
layers_json = json.dumps(flot_layers, indent=2)
template_str = template_str.replace('{{layers}}', layers_json)
template_str = template_str.replace('{{static}}', static_dir)
with open(os.path.expanduser('~/Desktop/out.html'), 'w') as f:
  f.write(template_str)
static_path = os.path.expanduser('~/Desktop/static')
if not os.path.exists(static_path):
  shutil.copytree('stuff/static', static_path)

# print 'slow regexes:'
# for regex, time in sorted(regex_to_time.iteritems(), key=lambda t: -t[1])[:10]:
#   print time, regex
