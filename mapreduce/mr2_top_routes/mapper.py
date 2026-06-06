#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()
    if not line: continue
    cols = line.split('\t')
    if len(cols) >= 14 and cols[0] != "ride_id":
        start_name = cols[6].strip()
        end_name = cols[8].strip()
        if start_name and end_name:
            print("{0} -> {1}\t1".format(start_name, end_name))