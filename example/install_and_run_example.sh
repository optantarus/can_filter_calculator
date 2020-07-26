 #!/bin/bash
 
 # Creates a virtual python environment, installs the script and executes it.
 
 # file to activate virtual python environment
 FILE=./env/bin/activate
 
 # check if virtual environment exists
 if [ -f $FILE ]
 then
    # activate environment
    source $FILE
 else
    # create environment and activate it
    python3 -m venv env
    source $FILE
    
    # install package and remove all generated files
    cd ..
    ./setup.py install
    ./setup.py clean --all
    rm -r dist
    rm -r  *.egg-info
    cd example
 fi
 

 # Execute example for can filter calculation
 # Needed input:
 #  -f  file with list of CAN ids in hex format
 #  -s  number of bits of CAN IDs (typically 11 or 29)
 #  -n  number of filters to calculate
 
 can_filter_calc -f=can_ids.txt -s=11 -n=2
 
 # close created virtual python environment
 deactivate
