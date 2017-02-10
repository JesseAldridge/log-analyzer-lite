import os, re, sys

path = os.path.expanduser('~/Desktop/mongodb.log.txt')
with open(path) as f:
    text = f.read()

ms_line = []
for line in text.splitlines():
    match = re.search('([0-9]+)ms', line)
    if match:
        ms_line.append((int(match.group(1)), line))

for ms, line in sorted(ms_line, key=lambda t: -t[0])[:100]:
    print '{}|{}'.format(ms, line)
