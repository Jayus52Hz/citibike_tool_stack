#!/usr/bin/env python3
import sys

current_hour, total_count = None, 0

for line in sys.stdin:
    line = line.strip()
    if not line: continue
    hour, count = line.split('\t')
    
    if current_hour == hour:
        total_count += int(count)
    else:
        if current_hour:
            print("{0}\t{1}".format(current_hour, total_count))
        current_hour = hour
        total_count = int(count)

if current_hour:
    print("{0}\t{1}".format(current_hour, total_count))