# Rules for Each Clause
'''
Clause	|Required?	    |Runs when?
try	    |Yes	        |Always — contains the code that might fail
except	|At least one	|When matching exception is raised in try
else	|No         	|Only if no exception was raised
finally	|No	            |Always — even if an unhandled exception propagates'''

# Exception Types Reference
'''
Exception	            |Trigger	                                    |Defensive Code Pattern
FileNotFoundError	    |open("x.txt", "r") — file missing          	|if Path("x.txt").exists(): ...
PermissionError	        |No rights to file/directory                   	|Catch and log; do not silently ignore
ValueError	            |int("abc"), bad conversion                 	|Validate before converting; catch in data-loading loops
KeyError	            |dict["missing"]	                            |dict.get("key", default)
IndexError	            |list[n] when n ≥ len(list)	                    |Check len() or iterate with for
TypeError	            |Wrong type for operation: len(42)          	|Type hints + validate at entry points
AttributeError	        |None.strip() — method on None              	|Check if x is not None:
json.JSONDecodeError	|Parsing invalid JSON	                        |Wrap json.loads() in try/except
UnicodeDecodeError	    |Wrong encoding specified for file             	|Try encoding="cp1252" or errors="replace"
OSError	                |Disk full, network FS unavailable, bad path	|Catch around all write operations
ZeroDivisionError	    |x / 0	                                        |Guard with if denominator != 0:'''
    
# Exception Hierarchy (simplified)
'''
BaseException
├── SystemExit          # sys.exit()
├── KeyboardInterrupt   # Ctrl+C
└── Exception           # ← Use this as your catch-all
    ├── OSError         # Includes FileNotFoundError, PermissionError
    ├── ValueError
    ├── TypeError
    ├── KeyError
    ├── IndexError
    └── AttributeError'''


# Log Levels Numeric Reference
'''
Level	|Value	|basicConfig level to capture it
DEBUG	|10	    |level=logging.DEBUG
INFO	|20	    |level=logging.INFO (default for production)
WARNING	|30	    |level=logging.WARNING (quiet mode)
ERROR	|40	    |Only errors and critical
CRITICAL|50	    |Only critical failures'''

# Format String Fields
'''
Field	        |Output	                            |Example
%(asctime)s	    |Timestamp (formatted by datefmt)	|2026-07-21 14:32:05
%(levelname)s	|Log level name	                    |INFO / WARNING
%(levelname)-8s	|Left-aligned, padded to 8 chars	|INFO
%(name)s	    |Logger name (from getLogger)	    |fintrust.pipeline
%(message)s	    |The log message	                |Processing file: data.csv
%(filename)s	|Source file name	                |clean_transactions.py
%(lineno)d	    |Line number in source	            |42
%(funcName)s	|Function name	                    |process_batch'''



import logging
import random
import logging
from pathlib import Path
import time

# One-time setup at the top of your script
logging.basicConfig(
    level=logging.DEBUG,           # Minimum level to capture
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(r"C:\Users\***********\Downloads\fintrust-cloud-portfolio\week_03\day_4\logs\practise.log"),   # Write to file
        logging.StreamHandler()                 # Also print to console
    ]
)

# Random integer between 1 and 100 (inclusive)
randomNum = random.randint(1, 100)
logging.info("Your random number is {}" .format(randomNum))
# try / except / else / finally — Structure Cheatsheet
try:
    num = int(input("Enter a number to divide the random number: "))
    result = randomNum / num
    logging.info("{} / {} = {}" .format(randomNum, num, result))
except ZeroDivisionError:
    logging.error("You can not divide by Zero")
except ValueError:
    logging.error("You can divide by a string enter a number")
except Exception:
    logging.error("Something went wrong, please ensure you enter a number more than zero ")
finally:
    name = input("Please enter your name: ")
    logging.info("Your name is: {}" .format(name))



