#!/usr/bin/env python3
import sys

current_error, error_count = None, 0

for line in sys.stdin:
    line = line.strip()
    if not line: continue
    err_type, count = line.split('\t')
    
    if current_error == err_type:
        error_count += int(count)
    else:
        if current_error:
            print("{0}\t{1}".format(current_error, error_count))
        current_error = err_type
        error_count = int(count)

if current_error:
    print("{0}\t{1}".format(current_error, error_count))