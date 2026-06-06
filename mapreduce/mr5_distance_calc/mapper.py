#!/usr/bin/env python3
import sys
import math

for line in sys.stdin:
    line = line.strip()
    if not line: continue
    cols = line.split('\t')
    if len(cols) >= 14 and cols[0] != "ride_id":
        try:
            start_name = cols[6].strip()
            end_name = cols[8].strip()
            if start_name and end_name:
                lat1, lng1 = float(cols[9]), float(cols[10])
                lat2, lng2 = float(cols[11]), float(cols[12])
                distance = math.sqrt((lat2 - lat1)**2 + (lng2 - lng1)**2) * 111
                print("{0} -> {1}\t1\t{2}".format(start_name, end_name, distance))
        except ValueError:
            continue