#!/usr/bin/env python3
import sys

current_status, total_count = None, 0

for line in sys.stdin:
    line = line.strip()
    if not line: continue
    status, count = line.split('\t')
    
    if current_status == status:
        total_count += int(count)
    else:
        if current_status:
            print("{0}\t{1}".format(current_status, total_count))
        current_status = status
        total_count = int(count)

if current_status:
    print("{0}\t{1}".format(current_status, total_count))