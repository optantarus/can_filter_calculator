rem Creates a virtual python environment, installs the script and executes it.
 
@rem file to activate virtual python environment
set FILE="env/Scripts/activate.bat"
 
@rem check if virtual environment exists
if exist %FILE% ( 
   @rem activate environment
   CALL %FILE%
) else (
   @rem create environment and activate it
   python -m venv env
   CALL %FILE%
   
   @rem install package and remove all generated files
   cd ..
   python setup.py install
   python setup.py clean --all
   RMDIR /S /Q dist
   RMDIR /S  /Q CAN_filter_calculator.egg-info
   cd example
)


@rem Execute example for can filter calculation
@rem Needed input:
@rem  -f  file with list of CAN ids in hex format
@rem  -s  number of bits of CAN IDs (typically 11 or 29)
@rem  -n  number of filters to calculate

can_filter_calc -f=can_ids.txt -s=11 -n=2

@rem close created virtual python environment
deactivate
