#!/usr/bin/env python3
import sys

current_route, total_trips, total_dist = None, 0, 0.0

for line in sys.stdin:
    line = line.strip()
    if not line: continue
    route, count, dist = line.split('\t')
    
    if current_route == route:
        total_trips += int(count)
        total_dist += float(dist)
    else:
        if current_route:
            avg_dist = round(total_dist / max(total_trips, 1), 3)
            print("{0}\t{1}\t{2}".format(current_route, avg_dist, total_trips))
        current_route = route
        total_trips = int(count)
        total_dist = float(dist)

if current_route:
    avg_dist = round(total_dist / max(total_trips, 1), 3)
    print("{0}\t{1}\t{2}".format(current_route, avg_dist, total_trips))