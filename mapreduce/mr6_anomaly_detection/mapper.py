#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()
    if not line: continue
    cols = line.split('\t')
    if len(cols) >= 14 and cols[0] != "ride_id":
        duration_str = cols[4].strip()
        end_lat_str = cols[11].strip()
        
        try:
            if float(duration_str) <= 0:
                print("BAD_DURATION_ERROR\t1")
        except ValueError:
            print("INVALID_DURATION_FORMAT\t1")
            
        if not end_lat_str or end_lat_str == "0" or end_lat_str.lower() == "null":
            print("MISSING_GPS_END_ERROR\t1")