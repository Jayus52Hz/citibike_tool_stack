#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()
    if not line: continue
    cols = line.split('\t')
    if len(cols) >= 14 and cols[0] != "ride_id":
        print("{0},{1}\t1\t{2}".format(cols[13].strip(), cols[1].strip(), cols[4].strip()))