#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()
    if not line: continue
    cols = line.split('\t')
    if len(cols) >= 14 and cols[0] != "ride_id":
        try:
            hour = cols[2].split(' ')[1].split(':')[0]
            print("{0}\t1".format(hour))
        except IndexError:
            continue