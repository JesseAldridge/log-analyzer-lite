import os, re, sys

path = '/Users/jessealdridge/Desktop/beta_heroku_drain_2017-02-09_080000_2017-02-10_080000.log'
path = os.path.expanduser(path)
with open(path) as f:
    text = f.read()

regex = '"url": "(.+?)",'

match_line = []
for line in text.splitlines():
    match = re.search(regex, line)
    if match:
        match_line.append((match.group(1), line))

for ms, line in sorted(match_line, key=lambda t: -t[0])[:100]:
    print '{}|{}'.format(ms, line)
