
# Turn timestamps into a consistent format
./normalize_timestamps.py ~/Desktop/mongodb.log.txt > ~/Desktop/norm.txt

# Group similar lines.  Create a file for each group: ~/Desktop/line_groups/*.txt
# this one is slow                         # only check every nth line
./group_similar_lines.py ~/Desktop/norm.txt 100

# For each group: create a regex to match all the lines the group
./lines_to_regex.py > ~/Desktop/regexes.txt

# Create a stack graph
./to_flot_format.py ~/Desktop/regexes.txt ~/Desktop/norm.txt
