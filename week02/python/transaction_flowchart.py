# Full structure
# if condition_A:
    # runs when A is True
# elif condition_B:
    # runs when A is False AND B is True
# elif condition_C:
    # runs when A and B are False AND C is True
# else:
    # runs when ALL conditions above are False

# You can have 0 or more elif branches
# The else branch is optional but recommended for "catch all"
# Python allows range checks in a single expression
amount = 7500

if 1000 <= amount < 10000:
    print("STANDARD transaction")

# Equivalent to:
if amount >= 1000 and amount < 10000:
    print("STANDARD transaction")

# Comparisons evaluate first: >, <, ==, !=, >=, <=
# Then: not
# Then: and
# Then: or (lowest)

# Without parentheses:
result = True or False and False
# Reads as: True or (False and False) = True or False = True

# With parentheses (recommended for clarity):
result = (True or False) and False  # = True and False = False
# Works with lists
BLOCKED = ["KP", "IR", "CU"]
print("IR" in BLOCKED)       # True
print("ZA" in BLOCKED)       # False
print("ZA" not in BLOCKED)   # True

# Works with strings
email = "thabo@fintrust.co.za"
print("fintrust" in email)   # True
print("@" in email)          # True

# Works with dictionaries (checks keys)
config = {"region": "af-south-1", "env": "prod"}
print("region" in config)    # True
print("timeout" in config)   # False
# Faster for large blocked lists
BLOCKED_COUNTRIES = {"KP", "IR", "CU", "SY", "SD"}  # set literal uses {}

destination = "IR"
if destination in BLOCKED_COUNTRIES:
    print("BLOCKED")

# Syntax: value_if_true if condition else value_if_false

# Example 1 — simple label
amount = 12000
label = "LARGE" if amount > 10000 else "STANDARD"
print(label)  # LARGE

# Example 2 — f-string embed
is_verified = True
msg = f"OTP {'sent' if is_verified else 'required'}"
print(msg)  # OTP sent

# Example 3 — function argument
def process(tx, urgent):
    queue = "FAST_LANE" if urgent else "STANDARD_QUEUE"
    print(f"Sending {tx} to {queue}")

# transaction_flowchart.py
# FinTrust Bank — Automated Transaction Decision Engine
# Week 2 Day 4 — Cloud to Solutions Accelerator

BLOCKED_COUNTRIES = ["KP", "IR", "CU", "SY", "SD"]
DAILY_LIMIT = 50000
LARGE_THRESHOLD = 10000
REVIEW_THRESHOLD = 5000


def assess_transaction(tx_id, customer, amount, destination, is_trusted_device):
    """
    Evaluate a FinTrust Bank transaction and return a decision dict.
    """

    # --- Hard blocks: check these first, return immediately ---

    # 1. Destination country check — always runs before amount checks
    #    because a blocked-country transfer should never proceed
    #    regardless of amount.
    if destination.upper() in BLOCKED_COUNTRIES:
        return {
            "tx_id": tx_id,
            "customer": customer,
            "status": "BLOCKED",
            "reason": f"Transfer to {destination} is not permitted"
        }

    # 2. Daily limit — absolute ceiling regardless of device trust
    if amount > DAILY_LIMIT:
        return {
            "tx_id": tx_id,
            "customer": customer,
            "status": "BLOCKED",
            "reason": f"Amount exceeds daily limit of R{DAILY_LIMIT:,.0f}"
        }

    # 3. Invalid amount guard
    if amount <= 0:
        return {
            "tx_id": tx_id,
            "customer": customer,
            "status": "BLOCKED",
            "reason": "Invalid transaction amount"
        }

    # --- Soft checks: outcome depends on device trust ---

    # 4. Large transfer (> R10 000)
    if amount > LARGE_THRESHOLD:
        if is_trusted_device:
            # Trusted device: allow with OTP step
            return {
                "tx_id": tx_id,
                "customer": customer,
                "status": "PENDING",
                "reason": "Large transfer — OTP verification required"
            }
        else:
            # Unrecognised device + large amount: flag for analyst
            return {
                "tx_id": tx_id,
                "customer": customer,
                "status": "REVIEW",
                "reason": "Large transfer from unrecognised device"
            }

    # 5. Moderate amount (> R5 000) on unrecognised device
    if amount > REVIEW_THRESHOLD and not is_trusted_device:
        return {
            "tx_id": tx_id,
            "customer": customer,
            "status": "REVIEW",
            "reason": "Moderate amount from unrecognised device"
        }

    # 6. Default: all checks passed
    return {
        "tx_id": tx_id,
        "customer": customer,
        "status": "APPROVED",
        "reason": "All checks passed"
    }


# --- Test Cases ---
test_cases = [
    ("TX001", "Thabo Nkosi",    500.00,   "ZA", True),   # APPROVED
    ("TX002", "Amahle Dlamini", 15000.00, "ZA", True),   # PENDING
    ("TX003", "Sipho Mokoena",  8000.00,  "ZA", False),  # REVIEW
    ("TX004", "Lerato Sithole", 200.00,   "IR", True),   # BLOCKED (country)
    ("TX005", "Nomvula Dube",   75000.00, "ZA", True),   # BLOCKED (limit)
]

print("=" * 65)
print(f"{'TX ID':<8} {'Customer':<18} {'Status':<10} Reason")
print("=" * 65)

for tc in test_cases:
    result = assess_transaction(*tc)
    print(f"{result['tx_id']:<8} {result['customer']:<18} {result['status']:<10} {result['reason']}")