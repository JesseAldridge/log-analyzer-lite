
# Turn timestamps into a consistent format
./normalize_timestamps.py ~/Desktop/csmk_heroku_drain_2016-05-04_211023_2016-05-05_211023.log

# Read norm.txt and build list of regexes that match similar lines
./lines_to_regex_simple.py 10000

# Create a stack graph (also slow)                          # only check every nth line
./to_flot_format.py ~/Desktop/regexes.txt ~/Desktop/norm.txt 100
