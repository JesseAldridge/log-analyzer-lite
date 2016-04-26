import os

with open(os.path.expanduser('~/Desktop/mongodb.log.txt')) as f:
    lines = f.read().splitlines()
print 'num lines:', len(lines)
count_by_hour = {}
for line in lines[:100000]:
    hour_str = line[:14]
    count_by_hour.setdefault(hour_str, [])
    count_by_hour[hour_str].append(line)

for key, lines in sorted(count_by_hour.iteritems(), key=lambda t: t[0]):
    # print '{} {}'.format(key, val)
    print key, '*' * (len(lines) / 1000)

