#!/usr/bin/python
import difflib, re, collections, json, sys

def strings_to_regex(string_list):
  # Tokenize and get diff opcodes for each of them.

  key_str = string_list[0]
  tokens_list = [re.findall(r'(\s+|\S+)', str_) for str_ in string_list[1:]]
  key_tokens = re.findall(r'(\s+|\S+)', key_str)

  list_of_codes = [
    [list(t) for t in
     difflib.SequenceMatcher(None, key_tokens, tokens).get_opcodes()]
    for tokens in tokens_list
  ]

  # Merge the opcodes for each string.

  merged_codes = []
  for _ in range(100):
    min_index, min_start, min_end = None, None, None
    for index, seq in enumerate(list_of_codes):
      if not seq:
        continue
      op_start, op_end = seq[0][1], seq[0][2]
      if op_start < min_start or min_start is None or (
        op_start == min_start and op_end < min_end):
        min_index = index
        min_start = op_start
        min_end = op_end
    if min_index is None:
      break
    merged_codes.append(list_of_codes[min_index][0])
    for i in range(len(list_of_codes)):
      if list_of_codes[i] and list_of_codes[i][0][1] == min_start:
        list_of_codes[i] = list_of_codes[i][1:]

  # print 'merged_codes:', merged_codes

  # Fix any overlap.
  for i in range(1, len(merged_codes)):
    # ['equal', 6, 8, 7, 9], ['insert', 7, 7, 7, 8]
    if merged_codes[i][1] < merged_codes[i - 1][2]:
      merged_codes[i - 1][2] = merged_codes[i][1]

  # print 'fixed overlap:', merged_codes

  # Escape regex chars.
  for i in range(len(key_tokens)):
    for ch in '()[]*+':
      key_tokens[i] = key_tokens[i].replace(ch, '\\' + ch)

  # Turn merged codes into regex.

  regex_tokens = []
  for code in merged_codes:
    if code[0] == 'equal':
      regex_tokens += key_tokens[code[1]:code[2]]
    elif code[0] in ('insert', 'delete'):
      regex_tokens[-1] += '.*?'
    elif code[0] == 'replace':
      regex_tokens.append('.*?')

  regex = ''.join(regex_tokens)
  # while re.search('\.\*\? *\.\*\?', regex):
  #     regex = re.sub('\.\*\? *\.\*\?', '.*?', regex)

  if regex == '.*?':
    print 'whatever regex'
    print '    key:', key_str
    for str_ in string_list:
      print '  other:', str_

  return regex

def test_strings(string_list):

  # Get the regex and verify that it matches each string.

  regex = strings_to_regex(string_list)
  print 'regex: ({})'.format(regex)
  for str_ in string_list:
    m = re.search(regex, str_)
    print m
    assert m
  print

def test():
  for string_list in [
    [
      "(The) attribute rdb was  not found on object cciss_cdp [from] dat device",
      "(The) magic attribute wtb was  not eaten on object foobar [from] device",
      "(The) tragic attribute xyzh was  not found on special object cciss_cd [from] device"
    ],
    ['The attribute rdc', 'The attribute wtb'],
    [
      '11:12:44,208 INFO zen.zenhubworker: Shutting down'
      '11:12:44,208 INFO zen.zenhubworker: Stopping reactor',
      '11:14:07,738 INFO zen.zenhubworker: Shutting down'
    ],
    [
      "ERROR zen.MinMaxCheck: User-supplied Python expression \(\(here.hw.totalMemory/1024 * 0.10\) - \(here.getRRDValue\('memBuffer'\) + here.getRRDValue\('memCached'\)\)\) for minimum value caused error: \['memAvailReal_memAvailReal'\]",
      "ERROR zen.MinMaxCheck: User-supplied Python expression ((here.hw.totalMemory/1024 * 0.10) - (here.getRRDValue('memBuffer') + here.getRRDValue('memCached'))) for minimum value caused error: ['memAvailReal_memAvailReal']"
    ],
    ['bigassstringwithoutnospaceswhatdo man', "bigbuttstringwithoutnospaceswhatdo mang"],
    [
      'INFO zen.ZenModeler: SNMP collection device il3ardapp03',
      'INFO zen.ZenModeler: SNMP collection device nm-vp-prod-wfe-c'
    ],
    ['single string']
  ]:
    test_strings(string_list)

def main():
  line_regexes = {}
  string_list = []
  for line in sys.stdin:
    line = line.strip('\n')
    if line == '\0':
      print strings_to_regex(string_list)
      string_list = []
      continue
    string_list.append(line)


if __name__ == '__main__':
  if len(sys.argv) > 1 and sys.argv[1] == 'test':
    test()
  else:
    main()
