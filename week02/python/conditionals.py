# Pattern: if → elif (as many as needed) → else
amount = 15000

if amount > 50000:
    print("BLOCKED: exceeds daily limit")
elif amount > 10000:
    print("PENDING: large transaction — OTP required")
elif amount > 0:
    print("APPROVED")
else:
    print("BLOCKED: invalid amount")

# ternary: value_if_true if condition else value_if_false
status = "HIGH_VALUE" if amount > 10000 else "NORMAL"
print(status)  # HIGH_VALUE

def classify_amount(amount):
    if amount <= 0:
        return "INVALID"
    elif amount <= 500:
        return "MICRO"
    elif amount <= 10000:
        return "STANDARD"
    else:
        return "LARGE"

print(classify_amount(750))   # STANDARD
print(classify_amount(0))     # INVALID

BLOCKED_COUNTRIES = ["KP", "IR", "CU", "SY", "SD"]

destination = "IR"

if destination in BLOCKED_COUNTRIES:
    print("BLOCKED: destination country not permitted")
else:
    print("Country check passed")

def initial_screen(amount, destination):
    BLOCKED_COUNTRIES = ["KP", "IR", "CU", "SY", "SD"]
    if destination.upper() in BLOCKED_COUNTRIES:
        return "BLOCKED", "Destination country not permitted"
    if amount > 50000:
        return "BLOCKED", "Exceeds daily transfer limit of R50 000"
    if amount <= 0:
        return "BLOCKED", "Invalid transaction amount"
    return "PASS", "Initial screen cleared"

status, reason = initial_screen(12000, "ZA")
print(status, "—", reason)  # PASS — Initial screen cleared

def assess_transaction(amount, destination, is_trusted_device):
    """
    Returns (status, reason) for a FinTrust transaction.
    """
    BLOCKED_COUNTRIES = ["KP", "IR", "CU", "SY", "SD"]

    # Hard blocks first
    if destination.upper() in BLOCKED_COUNTRIES:
        return ("BLOCKED", f"Transfer to {destination} is not permitted")

    if amount > 50000:
        return ("BLOCKED", "Amount exceeds daily limit of R50 000")

    if amount <= 0:
        return ("BLOCKED", "Invalid amount")

    # Soft checks — outcome depends on device trust
    if amount > 10000:
        if is_trusted_device:
            return ("PENDING", "Large transfer — OTP verification required")
        else:
            return ("REVIEW", "Large transfer from unrecognised device")

    if amount > 5000 and not is_trusted_device:
        return ("REVIEW", "Moderate amount from unrecognised device")

    # Default
    return ("APPROVED", "All checks passed")


# Test with Thabo Nkosi's transaction
status, reason = assess_transaction(8000, "ZA", False)
print(f"{status}: {reason}")
# REVIEW: Moderate amount from unrecognised device

"""Exercise 1 — Transaction Classifier
Write a function classify_transaction(amount) that returns a string based on these brackets:

0 < amount <= 100 → "MICRO"
100 < amount <= 1000 → "SMALL"
1000 < amount <= 10000 → "STANDARD"
amount > 10000 → "LARGE"
Any other value → "INVALID"
Test cases: classify_transaction(50) → "MICRO" | classify_transaction(9999) → "STANDARD" | classify_transaction(-5) → "INVALID"""

def classify_transaction(amount):
    if amount > 0 and amount <= 100:
        print("MICRO") 
    elif amount > 100 and amount <= 1000:
        print("SMALL") 
    elif amount > 1000 and amount <= 10000:
        print("STANDARD") 
    elif amount > 10000:
        print("LARGE") 
    else:
        print("INVALID") 
    
# OR 
def classify_trans(amnt):
    if 0 < amnt <= 100:
        print("MICRO") 
    elif 100 < amnt <= 1000:
        print("SMALL") 
    elif  1000 < amount <= 10000:
        print("STANDARD") 
    elif amount > 10000:
        print("LARGE") 
    else:
        print("INVALID") 

## Function Tests
print("Testing classify_transaction(amount) and classify_trans(amnt) Function ")
classify_transaction(50) 
classify_trans(150) 
classify_transaction(1550) 
classify_trans(15500) 
classify_trans(-50) 
print("___________________________________________________________________")    
    

'''Exercise 2 — Interest Rate Calculator
FinTrust charges different rates based on credit score. Write get_interest_rate(credit_score):

score >= 750 → 7.5 (prime rate)
700 <= score < 750 → 9.5
650 <= score < 700 → 12.0
score < 650 → 18.5
Test: get_interest_rate(720) → 9.5 | get_interest_rate(800) → 7.5'''
def get_interest_rate(credit_score):
    if credit_score >= 750:
        print(7.5)
    elif 700 <= credit_score < 750:
        print(9.5)
    elif 650 <= credit_score < 700:
        print(12.0)
    elif credit_score < 650:
        print(18.5)
    else:
        print("INVALID")

# Test function
print("Testing get_interest_rate(credit_score) Function ")
get_interest_rate(720)
get_interest_rate(800)
get_interest_rate(600)
get_interest_rate(666)
print("___________________________________________________________________")    

'''Exercise 3 — ATM Withdrawal Logic
Write atm_withdraw(balance, amount) that returns a tuple (success: bool, message: str):

If amount <= 0: (False, "Invalid amount")
If amount > 5000: (False, "ATM daily limit is R5 000")
If amount > balance: (False, "Insufficient funds")
Otherwise: (True, f"Dispensing R{amount:.2f}")
Test: atm_withdraw(3000, 1500) → (True, "Dispensing R1500.00") | atm_withdraw(500, 600) → (False, "Insufficient funds")'''
def atm_withdraw(balance, amount):
    if amount <= 0:
        return (False, "Invalid amount")
    elif amount > 5000:
        return (False, "ATM daily limit is R5 000")
    elif amount > balance:
        return (False, "Insufficient funds")
    else:
        return (True, f"Dispensing R{amount:.2f}")

# Test function
print("Testing atm_withdraw(balance, amount) Function ")
print(atm_withdraw(3000, 1500))
print(atm_withdraw(500, 600))
print(atm_withdraw(500, 0))
print(atm_withdraw(500, -600))
print(atm_withdraw(10000, 6000))
print("___________________________________________________________________")    

'''Exercise 4 — Transaction Tagger
Write tag_transaction(tx_type, merchant_category, amount) that returns a tag string. Rules:

If tx_type == "REFUND": return "REFUND"
If merchant_category == "GAMBLING": return "HIGH_RISK"
If merchant_category == "GROCERY" and amount < 500: return "ROUTINE"
If amount > 10000: return "LARGE_PURCHASE"
Default: return "STANDARD"'''
def tag_transaction(tx_type, merchant_category, amount):
    if tx_type.upper() == "REFUND":
        print("REFUND")
    elif merchant_category  == "GAMBLING":
        print("HIGH_RISK")
    elif merchant_category == "GROCERY" and amount < 500:
        print("ROUTINE")
    else:
        print("STANDARD")

# Test function
print("Testing tag_transaction(tx_type, merchant_category, amount) Function ")
tag_transaction("REFUND", "Clothes", 530)
tag_transaction("Purchase", "GAMBLING", 530)
tag_transaction("Purchase", "GROCERY", 350)
tag_transaction("Purchase", "GROCERY", 530)
tag_transaction("Purchase", "Clothes", 530)
tag_transaction("refund", "Clothes", 530)
print("___________________________________________________________________") 