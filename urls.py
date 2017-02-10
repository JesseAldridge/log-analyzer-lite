import os, re, sys, logging, shutil

log_path = os.path.expanduser('~/Desktop/log.txt')
shutil.move(log_path, log_path + '.old')
logging.basicConfig(filename=log_path, level=logging.DEBUG)

path = sys.argv[1]
path = os.path.expanduser(path)
with open(path) as f:
    text = f.read()

regex = '"url": "(.+?)",'

match_lines = []
for line in text.splitlines():
    match = re.search(regex, line)
    if match:
        match_lines.append([match.group(1), line])

common_prefix = None
for url, line in match_lines:
  logging.debug('url: {}'.format(url))
  logging.debug('common_prefix: {}'.format(common_prefix))
  if not common_prefix:
    common_prefix = url
    continue
  for i in range(min(len(url), len(common_prefix))):
    if url[i] != common_prefix[i]:
      break
  else:
    i += 1
  common_prefix = common_prefix[:i]
  if not common_prefix:
    break

logging.debug('prefix: {}'.format(common_prefix))

max_url_len = 0
for i, t in enumerate(match_lines):
  url, line = t
  match_lines[i][0] = url = url[len(common_prefix):]
  max_url_len = max(max_url_len, len(url))

for url, line in match_lines:
    print '{:<{}} | {}'.format(url, max_url_len, line)
