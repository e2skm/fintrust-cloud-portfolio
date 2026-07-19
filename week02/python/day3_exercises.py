# Exercise 1 — Account Formatter (10 min)
## Write a function format_account_summary(customer_name, account_type, balance) that returns a formatted string:

# Expected output:
# Customer: Thabo Nkosi
# Account:  SAVINGS
# Balance:  R 52,750.00
# Status:   ACTIVE

from decimal import Decimal

def format_account_summary(customer_name, account_type, balance):
    d_balance = Decimal(str(balance))

    return (
        f"Customer: {customer_name.title()}\n"
        f"Account:  {account_type.upper()}\n"
        f"Balance:  R {d_balance:,.2f}\n"
        f"Status:   ACTIVE"
    )

# Test
print(format_account_summary("thabo nkosi", "savings", 52750))
print('___________________________________________________________________________')

# Exercise 2 — Compound Interest

def calculate_compound_interest(principal, annual_rate, years, n=12):
    """
    principal: initial amount (Decimal)
    annual_rate: e.g. 0.085 for 8.5%
    years: number of years
    n: compounding periods per year (default 12 = monthly)
    """
    p = float(principal)

    amount = p * (1 + annual_rate / n) ** (n * years)
    interest_earned = amount - p

    return (
        Decimal(str(round(amount, 2))),
        Decimal(str(round(interest_earned, 2)))
    )

# Test
principal = Decimal("50000.00")
amount, interest = calculate_compound_interest(principal, 0.085, 3)

print(f"After 3 years: R {amount:,.2f}")
print(f"Interest earned: R {interest:,.2f}")
print('___________________________________________________________________________')
# Exercise 3 — List Operations

transactions = [
    Decimal("250.00"), Decimal("12500.00"), Decimal("750.50"),
    Decimal("88000.00"), Decimal("1200.00"), Decimal("3450.00"),
    Decimal("55000.00"), Decimal("125.00"), Decimal("9800.00")
]

# Calculate statistics
total = sum(transactions)
average = total / len(transactions)
largest = max(transactions)
smallest = min(transactions)
count_above_5000 = len([t for t in transactions if t > Decimal("5000.00")])

# Display results
print(f"Total: R {total:,.2f}")
print(f"Average: R {average:,.2f}")
print(f"Largest: R {largest:,.2f}")
print(f"Smallest: R {smallest:,.2f}")
print(f"Transactions above R 5,000: {count_above_5000}")
print('___________________________________________________________________________')