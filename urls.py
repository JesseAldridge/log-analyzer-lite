import os, re, sys, logging, shutil, textwrap

import jinja2

class LogLine:
  def __init__(self, line):
    self.line = line

    self.method = None
    match = re.search('"method": "([A-Z]+?)"', line)
    if match:
      self.method = match.group(1)

    self.url = None
    match = re.search('"url": "(.+?)",', line)
    if match:
        self.url = match.group(1)


def main():
  log_path = os.path.expanduser('~/Desktop/log.txt')
  shutil.move(log_path, log_path + '.old')
  logging.basicConfig(filename=log_path, level=logging.DEBUG)

  path = sys.argv[1]
  path = os.path.expanduser(path)
  with open(path) as f:
      text = f.read()

  log_lines = []
  for line in text.splitlines():
    if line:
      log_lines.append(LogLine(line))

  max_url_len = remove_common_url_prefix(log_lines)

  template = jinja2.Template(textwrap.dedent('''
    <style>
    * { font-family: Helvetica }

    table, td, th {
        border: 1px solid #ddd;
        text-align: left;
    }

    table {
        border-collapse: collapse;
        width: 100%;
    }

    th, td {
        padding: 15px;
    }
    </style>
    <table>
      <tr><th>method</th><th>url</th><th>full line</th></tr>
    {% for log_line in log_lines %}
      <tr>
        <td>{{log_line.method or ''}} </td>
        <td>{{log_line.url or ''}} </td>
        <td>{{log_line.line}}</td>
      </tr>
    {% endfor %}
    </table>
  '''))
  print template.render(log_lines=log_lines)


def remove_common_url_prefix(log_lines):
  common_url_prefix = None
  for log_line in log_lines:
    url = log_line.url
    if not url:
      continue
    logging.debug('url: {}'.format(url))
    logging.debug('common_url_prefix: {}'.format(common_url_prefix))
    if not common_url_prefix:
      common_url_prefix = url
      continue
    for i in range(min(len(url), len(common_url_prefix))):
      if url[i] != common_url_prefix[i]:
        break
    else:
      i += 1
    common_url_prefix = common_url_prefix[:i]
    if not common_url_prefix:
      break

  logging.debug('prefix: {}'.format(common_url_prefix))

  max_url_len = 0
  for log_line in log_lines:
    if not log_line.url:
      continue
    log_line.url = log_line.url[len(common_url_prefix):]
    max_url_len = max(max_url_len, len(log_line.url))
  return max_url_len

if __name__ == '__main__':
  main()
