# File Modes & open() Cheatsheet
'''Mode	Meaning	
"r"	Read text	
"w"	Write text	
"a"	Append text	
"x"	Exclusive create
"r+"	Read + write	
"rb"	Read binary	
"wb"	Write binary'''	
import csv

# write file.txt
with open(r"C:\Users\nb446086\Downloads\fintrust-cloud-portfolio\week_03\day_3\data\file.txt","w",newline="",encoding="utf-8") as f:
    fieldnames = ["name","gender","race","married", "age"]
    writer = csv.DictWriter(f,fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows([
        {"name": "James Brown","gender": "Male","race":"Black","married": False, "age": 77},
        {"name": "Helen Zeliar","gender": "Female","race": "White","married": True, "age": 56},
        {"name": "Money Cash","gender": "Male","race": "Asian","married": False, "age": 18},
        {"name": "Olivia Brown","gender": "Female","race": "Black","married": True, "age": 28},
        {"name": "Seth Smith","gender":"Non-Binary","race":"White","married": False, "age": 38}])

print("Reading file.txt ...")
# Correct — file is closed even if an exception is raised inside the block
with open(r"C:\Users\nb446086\Downloads\fintrust-cloud-portfolio\week_03\day_3\data\file.txt", "r", encoding="utf-8") as f:
    data = f.read()

# Wrong — if an exception is raised before f.close(), the file stays open
f = open(r"C:\Users\nb446086\Downloads\fintrust-cloud-portfolio\week_03\day_3\data\file.txt", "r", encoding="utf-8")
data = f.read()
f.close()

# Reading Methods
'''Method	|Returns	|When to use
f.read()	|Entire file as one string	|Small files where you need the whole content
f.readlines()	|List of lines (with \n)	|When you need indexed access to lines
for line in f:	|One line at a time	|Large files — memory efficient; use line.strip()
f.readline()	|Single next line	|Rare — when parsing line-by-line conditionally'''

# csv Module Cheatsheet
import csv
# The Two Reader Classes
# Write file.csv
print("Writting file.csv .....")
with open("file.csv", "w", newline="", encoding="utf-8") as f:
    fieldnames = ["account_id","amount"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows([
        {"account_id":"SA-987563", "amount":1444.45},
        {"account_id":"CH-676767", "amount":99999999.99},
        {"account_id":"DB-465632", "amount":12000.00}])

# 1. csv.reader — rows as lists, access by index: row[0], row[1]
print("Reading file.csv .....")
with open("file.csv", "r", newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    headers = next(reader)   # Skip header row
    for row in reader:
        print(row[0], row[1])

# 2. csv.DictReader — rows as dicts, access by column name (Recommended)
with open("file.csv", "r", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["account_id"], row["amount"])

print("Writting out.csv")
# The Two Writer Classes
# 1. csv.writer — write lists
with open("out.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "name", "amount"])    # header
    writer.writerows([[1, "Thabo", 5000.00], [2, "Amara", 7500.00]])

# 2. csv.DictWriter — write dicts (Recommended for readability)
with open("out.csv", "w", newline="", encoding="utf-8") as f:
    fieldnames = ["id", "name", "amount"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows([
        {"id": 1, "name": "Thabo", "amount": 5000.00},
        {"id": 2, "name": "Amara", "amount": 7500.00},
    ])

# Read the out.csv 
print("Reading out.csv ......")
with open("out.csv", "r", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["id"],row["name"],row["amount"])


# Handling Different Delimiters
# CSV files sometimes use semicolons (common in European/ZA exports)
'''reader = csv.DictReader(f, delimiter=";")'''

# Custom quoting character
'''reader = csv.DictReader(f, quotechar="'")'''

# json Module Cheatsheet
import json
# Four Core Functions
"""Function	|Input	|Output	|Use for
json.load(f)	|File object	|Python dict/list	|Reading a JSON file
json.dump(obj, f)	|Object + file	Writes to file	|Writing a JSON file
json.loads(s)	|JSON string	|Python dict/list	|Parsing API responses, config strings
json.dumps(obj)	|Python object	|JSON string	|Sending to API, embedding in HTTP body"""

# Type Mapping: Python ↔ JSON
# Python type	JSON equivalent	Notes
'''dict	Object {}	Keys must be strings in JSON
list	Array []	
str	String ""	
int / float	Number	float can have precision issues — use Decimal for money
True / False	true / false	Lowercase in JSON
None	null	
datetime	Not natively supported	Convert to string: dt.isoformat()
Decimal	Not natively supported	Convert to string: str(decimal_val)'''

# Useful dump Options
data = {"name": "Thabo", "amount": 5000.00}
json.dumps(data)                    # {"name": "Thabo", "amount": 5000.0}
json.dumps(data, indent=2)          # Pretty-printed (human readable)
json.dumps(data, sort_keys=True)    # Keys in alphabetical order
json.dumps(data, ensure_ascii=False) # Allow UTF-8 chars like ë, ü

# Write input.csv
print("Wrtting input.csv")
with open("input.csv", "w", newline="", encoding="utf-8") as f:
    fieldnames = ["id", "name", "amount"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows([
        {"id": 1, "name": "Nompilo", "amount": 1874303708235000.00},
        {"id": 2, "name": "Akhona", "amount": 924857942947500.00},
        {"id": 3, "name": "Nolwazi", "amount": 983474315000.00},
        {"id": 4, "name": "Tshifiwa", "amount": 75019384982300.00},
        {"id": 5, "name": "Sandeep", "amount": 594389000.00},
        {"id": 6, "name": "Shuan", "amount": 9001927500.00},
        {"id": 7, "name": "Mikateko", "amount": 46180174055000.00},
        {"id": 8, "name": "Zakhele", "amount": 719332187431500.00},
        {"id": 9, "name": "Itumeleng", "amount": 9999500000000000000.00}])

# Read CSV → Filter → Write CSV
with open("input.csv", "r", newline="", encoding="utf-8") as fin, \
    open("output.csv", "w", newline="", encoding="utf-8") as fout:

    reader = csv.DictReader(fin)
    writer = csv.DictWriter(fout, fieldnames=reader.fieldnames)
    writer.writeheader()

    for row in reader:
        if float(row["amount"]) > 1000:
            writer.writerow(row)
# OR

with (
    open("input.csv", "r", newline="", encoding="utf-8") as fin,
    open("output.csv", "w", newline="", encoding="utf-8") as fout,
):
    reader = csv.DictReader(fin)
    writer = csv.DictWriter(fout, fieldnames=reader.fieldnames)
    writer.writeheader()

    for row in reader:
        if float(row["amount"]) > 1000:
            writer.writerow(row)

# Read CSV → Convert to JSON
print("Reading input.csv and converting to input.json ...")
from pathlib import Path
with open(r"C:\Users\nb446086\Downloads\fintrust-cloud-portfolio\week_03\day_3\data\input.csv", "r", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    records = list(reader)   # materialise to list of dicts

Path("input.json").write_text(
    json.dumps(records, indent=2),
    encoding="utf-8"
)

# Read JSON Config → Use in Script
print("Reading config.json ....")
config = json.loads(Path(r"C:\Users\nb446086\Downloads\fintrust-cloud-portfolio\week_03\day_3\data\config.json").read_text(encoding="utf-8"))
bucket = config["buckets"]["transactions"]
region = config["region"]
print(bucket)  
print(region)

# Append to JSON Log (Line-delimited NDJSON)
def append_log(filepath, record):
    """Append one JSON object per line — easy to stream and parse."""
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")

# Test data
append_log("test.log", {"id": 1, "amount": 100.50})
append_log("test.log", {"id": 2, "amount": 250.75})

# Verify contents
with open("test.log", "r", encoding="utf-8") as f:
    print(f.read())

# Common Errors & Fixes
"""Error	|Cause	|Fix
FileNotFoundError	|Path is wrong, file does not exist, script run from wrong directory	|Use Path(__file__).parent / "filename" for paths relative to the script. Print Path.cwd() to check working directory.
UnicodeDecodeError	|File encoding doesn't match encoding= parameter (common with Windows cp1252 files)	|Try encoding="cp1252" or encoding="latin-1". Or open with errors="replace" to skip bad characters.
json.JSONDecodeError	|File is not valid JSON — truncated, has trailing comma, or is empty	|Validate with python -m json.tool file.json on command line.
csv: extra blank rows	|Missing newline="" on Windows	|Add newline="" to open() for all CSV files.
KeyError on DictReader	|Column name has leading/trailing spaces or different case	Print reader.fieldnames to see exact header names. |Strip + lower: {k.strip().lower(): v for k,v in row.items()}
TypeError: Object of type X is not JSON serializable	|datetime or Decimal in the dict being serialised	|Convert before dumping: dt.isoformat(), str(decimal_val), or write a custom encoder.
PermissionError	|File is open in another program (e.g., Excel has it locked)	|Close the file in the other application. On Windows, Excel holds a lock on open CSV files"""

# Quick Diagnosis Pattern: 
'''If a file operation fails, print the absolute path you're using (print(Path("file.csv").resolve())) 
and the current working directory (print(Path.cwd())). 80% of file errors are wrong paths.'''