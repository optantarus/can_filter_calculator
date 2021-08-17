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

This tool uses the More Itertools library.

The idea to use the simulated annealing algorithm comes from the following paper:

> Florian Pölzlbauer, Robert I. Davis, and Iain Bate. 2017. Analysis and
> Optimization of Message Acceptance Filter Configurations for Controller
> Area Network (CAN). In Proceedings of RTNS ’17, Grenoble, France, October
> 4–6, 2017, 10 pages.
> <https://doi.org/10.1145/3139258.3139266>


## Prerequisities

- Python3
<http://www.python.org/getit/>

- More Itertools
<https://github.com/more-itertools/more-itertools>


## Usage

can_filter_calc.py is a command line tool. It needs to be called with the following information

- '-f'    file with CAN IDs (one ID per line in hex format)  
- '-s'    bit size of the CAN IDs (11 or 29)  
- '-n'    number of filters to use  
- '-o'    file to write results to (optional)  
- '-a'    algorithm to use (optional): OPT tries all posibilities, SA uses simulated annealing to find a solution  

So for example:  can_filter_calc.py -f=can_ids.txt -s=11 -n=2

It outputs the following to console window:

   > Result:
   > 
   > Lists:  [['00000111111', '00000010101'], ['00000000010']] 
   > 
   > Filters:  ['00000X1X1X1', '00000000010'] 
   > 
   > Sum messages pass:  6
   
Lists  (a list of lists) shows the used partitioning of the CAN IDs. So the first list corresponds to the first filter.

Filters shows the calculated CAN filters. The can filter is represented as a string.
'0' or '1' means an CAN ID has to have that value. 'X' means don't care.

Sum messages pass is the complete number of CAN IDs that can pass the calculated filters and are not specified in CAN ID list.

If specified  a file is created in addition. It contains the following:

   > Calculated CAN Filters [ filter : number of unwanted passing messages ]:  
   > 0b00000X1X1X1 :     6 | 0b00000000010 :     0  
   > 
   > CAN messages assigned to filters [ bin : hex ]:  
   > 0b00000111111 : 0x03f | 0b00000000010 : 0x002  
   > 0b00000010101 : 0x015 |  

Each column shows the calculated filter at the top and then all CAN message IDs used to calculate that filter.


Also take a look at the example folder.


## MAP OF FILES

```
+-- can_filter_calc/ —> folder with python script
|   +-- can_filter_calc.py
|
+-- example/ —> folder to show usage
|   +-- can_ids.txt    -> file with example CAN IDs
|   +-- run_example.sh -> execute can_filter_calc.py
|   +-- install_run_example.sh -> create virtual environment, install package with setuy.py and execute can_filter_calc
|
+-- test/ -> folder with unit tests
|   +-- test_can_ids_29bit.txt -> file with 29 bit CAN IDs for unit tests
|   +-- test_can_ids_11bit.txt -> file with 11 bit CAN IDs for unit tests
|   +-- test_can_filter_calc.py -> file with unit tests
|   +-- result_test_*.txt -> output files of the test cases
|
+-- LICENSE.txt —> License agreement
|
+-- README.md —> general information
|
+-- setup.cfg —> general configuration
|
+-- setup.py —> setuptools configuration
|
+-- requirements.txt —> required packages to run can_filter_calc
|
+-- .project      -> Eclipse Pydev project files
+-- .pydevproject -> Eclipse Pydev project files
```
