#!/usr/bin/env python3
import sys

current_key, total_trips, total_time = None, 0, 0.0

for line in sys.stdin:
    line = line.strip()
    if not line: continue
    key, count, duration = line.split('\t')
    
    if current_key == key:
        total_trips += int(count)
        total_time += float(duration)
    else:
        if current_key:
            avg_time = round(total_time / max(total_trips, 1), 2)
            print("{0}\t{1}\t{2}".format(current_key, avg_time, total_trips))
        current_key = key
        total_trips = int(count)
        total_time = float(duration)

if current_key:
    avg_time = round(total_time / max(total_trips, 1), 2)
    print("{0}\t{1}\t{2}".format(current_key, avg_time, total_trips))