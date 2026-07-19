# FinTrust Banking: Python data types in context

# str — customer names, account numbers, status strings
customer_name = "Thabo Nkosi"
account_number = "FT-0042-ZA"
status = "active"

# int — counts, IDs, whole numbers only
customer_id = 1001
transaction_count = 47
fraud_score = 85       # 0-100 scale

# float — use for scientific calculations ONLY
# NEVER use float for money (binary approximation errors)
interest_rate = 0.085  # 8.5% — float is ok here (rate, not amount)

# Decimal — ALWAYS use for monetary amounts
from decimal import Decimal
balance = Decimal("52750.00")      # R 52,750.00
transaction_amount = Decimal("1250.50")

# bool — flags, conditions
is_verified = True
is_blocked = False
has_overdraft = False

# list — ordered collection
provinces = ["Gauteng", "KwaZulu-Natal", "Western Cape"]
blocked_countries = ["NG", "RU", "KP", "IR"]

# dict — key-value pairs, like a record
customer = {
    "id": 1001,
    "name": "Thabo Nkosi",
    "province": "Gauteng",
    "balance": Decimal("52750.00"),
    "is_verified": True
}
from decimal import Decimal

balance = Decimal("52750.00")
deposit = Decimal("5000.00")
fee = Decimal("12.50")

new_balance = balance + deposit - fee    # Decimal("57737.50")
fee_percent = fee / balance * 100        # Very small percentage

# Integer division and modulo
total_transactions = 47
pages = total_transactions // 10         # 4 (whole pages)
remainder = total_transactions % 10      # 7 (transactions on last page)

print(f"New balance: R {new_balance:,.2f}")  # R 57,737.50
# Customer name formatting
raw_name = "  thabo NKOSI  "
clean_name = raw_name.strip()         # "thabo NKOSI" — remove whitespace
title_name = clean_name.title()       # "Thabo Nkosi" — title case
upper_name = clean_name.upper()       # "THABO NKOSI"
lower_name = clean_name.lower()       # "thabo nkosi"

# String length
account_number = "FT-0042-ZA"
print(len(account_number))            # 10

# Check contents
if account_number.startswith("FT-"):
    print("Valid FinTrust account number")

# Replace
dirty_input = "Thabo-Nkosi"
clean = dirty_input.replace("-", " ")  # "Thabo Nkosi"

# Split — parse CSV-style data
csv_row = "1001,Thabo,Nkosi,Gauteng"
fields = csv_row.split(",")           # ["1001", "Thabo", "Nkosi", "Gauteng"]
customer_id = int(fields[0])          # 1001 (as integer)

# f-strings — the professional way to format strings
first_name = "Amahle"
last_name = "Dlamini"
balance = 78500.00

greeting = f"Welcome back, {first_name} {last_name}!"
balance_msg = f"Your balance: R {balance:,.2f}"
print(greeting)    # Welcome back, Amahle Dlamini!
print(balance_msg) # Your balance: R 78,500.00
# THE TRAP:
amount_str = input("Enter deposit amount: ")  # User types: 1000
# amount_str is "1000" (a string, not an integer!)

# result = amount_str + 500  # TypeError: can only concatenate str (not int) to str
# OR worse:
# result = amount_str + "500"  # "1000500" — string concatenation!

# THE FIX: Convert immediately
# amount = float(input("Enter deposit amount: "))  # Still not ideal for money
# BEST: Use Decimal for money
from decimal import Decimal
amount = Decimal(input("Enter deposit amount: "))  # "1000" -> Decimal("1000")
str_num = "42"
integer = int(str_num)          # 42
decimal_val = float(str_num)    # 42.0

num = 1234
as_string = str(num)            # "1234"

from decimal import Decimal
exact_money = Decimal("1234.56")
as_float = float(exact_money)   # 1234.56 (loses precision — avoid for final storage)
