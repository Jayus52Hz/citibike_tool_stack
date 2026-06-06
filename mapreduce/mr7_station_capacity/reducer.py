#!/usr/bin/env python3
import sys

current_group, total_count = None, 0

for line in sys.stdin:
    line = line.strip()
    if not line: continue
    group, count = line.split('\t')
    
    if current_group == group:
        total_count += int(count)
    else:
        if current_group:
            print("{0}\t{1}".format(current_group, total_count))
        current_group = group
        total_count = int(count)

if current_group:
    print("{0}\t{1}".format(current_group, total_count))