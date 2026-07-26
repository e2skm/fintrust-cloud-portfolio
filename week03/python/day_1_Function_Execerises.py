def greet_customer(name):
    """Return a greeting string for a FinTrust customer."""
    return f"Welcome back, {name}. Your account is active."

# Call the function
message = greet_customer("Thabo Nkosi")
print(message)  # Welcome back, Thabo Nkosi. Your account is active.

def format_account_summary(customer_name, account_type, balance):
    """Format a short account summary line."""
    return f"{customer_name} | {account_type.upper()} | R {balance:,.2f}"

print(format_account_summary("Amahle Dlamini", "savings", 45230.75))
# Amahle Dlamini | SAVINGS | R 45,230.75

def calculate_interest(balance, rate=0.065, months=12):
    """Calculate simple interest on a FinTrust savings account."""
    return balance * rate * (months / 12)

# Use defaults
interest = calculate_interest(10000)          # rate=0.065, months=12
# Override one default
interest = calculate_interest(10000, months=6) # rate=0.065, months=6
# Override both
interest = calculate_interest(10000, 0.072, 3)

def create_transaction(account_id, amount, transaction_type, description=""):
    """Create a transaction record dict."""
    return {
        "account_id": account_id,
        "amount": amount,
        "type": transaction_type,
        "description": description
    }

# Positional (order matters)
tx = create_transaction(101, 5000.00, "deposit")

# Keyword (order doesn't matter, more readable)
tx = create_transaction(
    account_id=101,
    transaction_type="withdrawal",
    amount=250.00,
    description="ATM withdrawal Sandton City"
)

def get_account_status(balance, overdraft_limit=-500):
    """Return status string and whether account needs attention."""
    if balance >= 0:
        return "healthy", False
    elif balance >= overdraft_limit:
        return "overdrawn", True
    else:
        return "suspended", True

status, needs_attention = get_account_status(-200)
print(status)          # overdrawn
print(needs_attention) # True


# Exercises:
"""EX1
Write a function
calculate_monthly_fee(account_type)
that returns R 0 for "savings", R 65 for "cheque", and R 120 for "credit".""" 
def calculate_monthly_fee(account_type):
    if account_type.lower() == "savings":
        print('R 0')
    elif account_type.lower() == "cheque":
        print('R 65')
    elif account_type.lower() == "credit":
        print('R 120')
    else:
        print(f"Invalid account type; {account_type} doesn't exist")


# Test cases
print("Testing calculate_monthly_fee() Function")
calculate_monthly_fee("Savings")
calculate_monthly_fee("CHEQUE")
calculate_monthly_fee("Credit")
calculate_monthly_fee("Debit")
calculate_monthly_fee("Saving")
print("_____________________________________________")

"""EX2
Write a function
mask_id_number(id_number)
that returns the ID with the middle 6 digits replaced by asterisks:
"8501015009084"
→
"850101******4".""" 

def mask_id_number(id_number):
    id_number = id_number.replace(" ", "")

    if len(id_number) != 13:
        return "Invalid ID number"

    masked_id_number = ""

    for i in range(len(id_number)):
        if 6 <= i <= 11:  # middle 6 digits
            masked_id_number += "*"
        else:
            masked_id_number += id_number[i]

    return masked_id_number    
# Test cases
print("Testing mask_id_number() Function")
print(mask_id_number("0203045611086"))
print(mask_id_number("8501015009084"))
print(mask_id_number("850101500908"))
print(mask_id_number("9501015009084"))
print(mask_id_number("BSOIOISOOPOBF"))
print("_____________________________________________")
    

"""EX3
Write a function
summarise_transactions(transactions)
that takes a list of amounts and returns a tuple
(total_in, total_out, net)
where deposits are positive and withdrawals are negative.""" 

def summarise_transactions(transactions):
    total_in = 0
    total_out = 0

    for amount in transactions:
        if amount > 0:
            total_in += amount
        elif amount < 0:
            total_out += amount

    net = total_in + total_out

    return (total_in, total_out, net)
# Test cases
transactions = [1000, -250, 500, -100]
print(summarise_transactions(transactions))
transactions = [200, 300, 100]
print(summarise_transactions(transactions))
transactions = [-50, -25, -75]
print(summarise_transactions(transactions))
transactions = []
print(summarise_transactions(transactions))
transactions = [1000, -500, 200, -100, -50]
print(summarise_transactions(transactions))
print("_____________________________________________")