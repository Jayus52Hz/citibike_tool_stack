#!/usr/bin/env python3
import sys

current_key, total_count = None, 0

for line in sys.stdin:
    line = line.strip()
    if not line: continue
    key, count = line.split('\t')
    
    if current_key == key:
        total_count += int(count)
    else:
        if current_key:
            day, user = current_key.split(',')
            print("{0}\t{1}\t{2}".format(day, user, total_count))
        current_key = key
        total_count = int(count)

if current_key:
    day, user = current_key.split(',')
    print("{0}\t{1}\t{2}".format(day, user, total_count))