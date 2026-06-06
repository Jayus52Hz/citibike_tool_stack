#!/usr/bin/env python3
import sys
from datetime import datetime

for line in sys.stdin:
    line = line.strip()
    if not line: continue
    cols = line.split('\t')
    if len(cols) >= 14 and cols[0] != "ride_id":
        try:
            date_str = cols[2].split(' ')[0]
            day_name = datetime.strptime(date_str, "%Y-%m-%d").strftime("%A")
            print("{0},{1}\t1".format(day_name, cols[13].strip()))
        except ValueError:
            continue