 #!/bin/bash
 
 # Execute example for can filter calculation
 # Needed input:
 #  -f  file with list of CAN ids in hex format
 #  -s  number of bits of CAN IDs (typically 11 or 29)
 #  -n  number of filters to calculate
 
 ../can_filter_calc/can_filter_calc.py -f=can_ids.txt -s=11 -n=2
