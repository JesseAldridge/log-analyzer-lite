import os, re, sys

path = sys.argv[1]
with open(path) as f:
    text = f.read()

for line in text.splitlines():
    # if 'web.18' in line or not re.search(r'web\.[0-9]+', line):
    if 'chord_unlock' in line:
        clean_line = line
        if 'request_url' in line:
            try:
                clean_line = re.search("request_url.+?'.+?'", clean_line).group()
            except:
                print 'fail:', clean_line
                break
        print clean_line
