import os, re, sys

# 308 <190>1 2017-02-25T04:59:45.643241+00:00 app worker_p0.1 - - [2017-02-25 04:59:45,642: ERROR/Worker-6] tasks.ticket.create_tickets_from_subscription_task.CreateTicketTask[ceff2fe4-52df-4e27-a

path = sys.argv[1]
with open(os.path.expanduser(path)) as f:
    lines = f.read().splitlines()
print 'num lines:', len(lines)
count_by_hour = {}
max_count = 1
for line in lines[:100000]:
    match = re.search('[0-9]{4}-[0-9]{2}-[0-9]{2}(T| )[0-9]+:[0-9]', line)
    if not match:
      continue
    hour_str = match.group()
    count_by_hour.setdefault(hour_str, [])
    count_by_hour[hour_str].append(line)
    max_count = max(len(count_by_hour[hour_str]), max_count)

for key, lines in sorted(count_by_hour.iteritems(), key=lambda t: t[0]):
    # print '{} {}'.format(key, val)
    print key, '*' * (len(lines) / max_count * 20), len(lines)

