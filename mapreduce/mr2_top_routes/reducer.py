#!/usr/bin/env python3
import sys

current_route, total_count = None, 0

for line in sys.stdin:
    line = line.strip()
    if not line: continue
    route, count = line.split('\t')
    
    if current_route == route:
        total_count += int(count)
    else:
        if current_route:
            print("{0}\t{1}".format(current_route, total_count))
        current_route = route
        total_count = int(count)

if current_route:
    print("{0}\t{1}".format(current_route, total_count))