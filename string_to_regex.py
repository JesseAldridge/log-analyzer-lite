import re, collections

class Token:
    def __init__(self, s, is_matched):
        self.s = s
        self.is_matched = is_matched

def regex_escape(s):
  for ch in '\\()[]{}*+-^$?.|/':
    s = s.replace(ch, '\\' + ch)
  return s

def string_to_regex(original_s):
    escaped_s = regex_escape(original_s)
    regex = _string_to_regex(escaped_s, ['[a-z0-9]{24,}', '[0-9]{2,}'])
    assert re.match(regex, original_s)
    return regex

def _string_to_regex(original_s, regexes):
    if not regexes:
        return original_s
    substrs = []
    regex = regexes[0]
    for i, s in enumerate(re.split('(' + regex + ')', original_s)):
        if not s:
            continue
        if i % 2 == 0:  # (regular unmatched substring)
            substrs.append(_string_to_regex(s, regexes[1:]))
        else: # (matched regex substring)
            substrs.append(regex)
    full_regex = ''.join(substrs)
    return full_regex

if __name__ == '__main__':
    print string_to_regex('''[conn17519965] update gigwalk_apps_1.query_cache query: { collection: "data_items", signature: "4a45ff38fd6be0af98e3534ae4f5b88f" } update: { collection: "data_items", tag: ObjectId('571a0ca84f4ca7000e7f9430'), updatedAt: new Date(1461573452261), signature: "4a45ff38fd6be0af98e3534ae4f5b88f", data: { result: [], ok: 1.0 } } nMatched:1 nModified:0 upsert:1 keyUpdates:0 numYields:0 locks(micros) w:234722 117ms''')

