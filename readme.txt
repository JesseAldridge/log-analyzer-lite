
# Turn timestamps into a consistent format
./normalize_timestamps.py ~/Desktop/mongodb.log.txt > ~/Desktop/norm.txt

# Group similar lines.  Create a file for each group: ~/Desktop/line_groups/*.txt
# this one is slow                         # only check every nth line
./group_similar_lines.py ~/Desktop/norm.txt 100

# Create a regex to match all the lines in a group
./lines_to_regex.py
