#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()
    if not line: continue
    cols = line.split('\t')
    
    if len(cols) >= 12 and cols[0] != "station_id":
        try:
            capacity = int(float(cols[5].strip()))
            if capacity < 20:
                group = "SMALL_STATION (<20)"
            elif capacity <= 40:
                group = "MEDIUM_STATION (20-40)"
            else:
                group = "LARGE_STATION (>40)"
            print("{0}\t1".format(group))
        except ValueError:
            continue