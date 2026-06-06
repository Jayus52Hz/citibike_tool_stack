#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()
    if not line: continue
    cols = line.split('\t')
    
    if len(cols) >= 12 and cols[0] != "station_id":
        is_installed = cols[8].strip()
        is_renting = cols[9].strip()
        
        if is_installed == "1" and is_renting == "1":
            status = "ACTIVE_STATION"
        else:
            status = "MAINTENANCE_OR_LOCKED_STATION"
        print("{0}\t1".format(status))