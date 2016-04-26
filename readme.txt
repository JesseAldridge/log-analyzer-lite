

./normalize_timestamps.py ~/Desktop/mongodb.log.txt > ~/Desktop/norm.txt

# this one is slow                         # only check every nth line
./group_similar_lines.py ~/Desktop/norm.txt 100

