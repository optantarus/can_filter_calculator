# CAN Filter Calculator

## Introduction

Microcontrollers with CAN hardware offer the possibility to set filters for the received CAN messages.
They should be set so that as few as possible unwanted CAN messages pass to reduce the load of the controller.

This tool takes a list of CAN message IDs and tries to find filters with as few passing messages as possible.
The number of filters to use has to be specified.

The tool outputs the filter as strings with '0', '1' and 'X'. You have to translate this to the format needed
by the used controller.

For license information see LICENSE.txt.


## Acknowledgments

This tool uses the More Itertools library. Thanks to its developers.


## Prerequisities

- Python3
http://www.python.org/getit/

- More Itertools
https://github.com/more-itertools/more-itertools


## Usage

can_filter_calc.py is a command line tool. It needs to be called with the following information

- '-f'    file with CAN IDs (one ID per line in hex format)  
- '-s'    bit size of the CAN IDs (11 or 29)  
- '-n'    number of filters to use  

So for example:  can_filter_calc.py -f=can_ids.txt -s=11 -n=2

It outputs the following:

   > Result:
   > 
   > Lists:  [['00000111111', '00000010101'], ['00000000010']] 
   > 
   > Filters:  ['00000X1X1X1', '00000000010'] 
   > 
   > Sum messages pass:  3
   
Lists  (a list of lists) shows the used partitioning of the CAN IDs. So the first list corresponds to the first filter.

Filters shows the calculated CAN filters. The can filter is represented as a string.
'0' or '1' means an CAN ID has to have that value. 'X' means don't care.

Sum messages pass is the complete number of CAN IDs that can pass the calculated filters and are not specified in CAN ID list.


Also take a look at the example folder.


## MAP OF FILES

```
+-- can_filter_calc/ —> folder with python script
|   +-- can_filter_calc.py
|
+-- example/ —> folder to show usage
|   +-- can_ids.txt    -> file with example CAN IDs
|   +-- run_example.sh -> execute can_filter_calc.py
+-- LICENSE.txt —> License agreement
|
+-- README.md —> general information
|
+-- .project      -> Eclipse Pydev project files
+-- .pydevproject -> Eclipse Pydev project files
```
