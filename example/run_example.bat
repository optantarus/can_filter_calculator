echo off
rem Execute example for can filter calculation
rem Needed input:
rem  -f  file with list of CAN ids in hex format
rem  -s  number of bits of CAN IDs (typically 11 or 29)
rem  -n  number of filters to calculate

echo on 

python ../can_filter_calc/can_filter_calc.py -f=can_ids.txt -s=11 -n=2