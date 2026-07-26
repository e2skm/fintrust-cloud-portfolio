# File: fintrust_utils.py
"""Utility functions for FinTrust data processing."""

SOUTH_AFRICAN_PROVINCES = [
    "Gauteng", "Western Cape", "KwaZulu-Natal",
    "Eastern Cape", "Limpopo", "Mpumalanga",
    "North West", "Free State", "Northern Cape"
]

def format_rand(amount):
    """Format a decimal as South African Rand."""
    return f"R {amount:,.2f}"

def validate_id_number(id_number):
    """Check basic SA ID number format (13 digits, numeric)."""
    return len(str(id_number)) == 13 and str(id_number).isdigit()

def categorise_transaction(amount):
    """Return transaction category based on amount."""
    abs_amount = abs(amount)
    if abs_amount < 500:
        return "small"
    elif abs_amount < 5000:
        return "medium"
    else:
        return "large"
    
# File: main.py — import and use the module
import fintrust_utils

print(fintrust_utils.format_rand(1234567.89))  # R 1,234,567.89
print(fintrust_utils.validate_id_number("8501015009084"))  # True

# Or import specific names
from fintrust_utils import format_rand, categorise_transaction
print(format_rand(450.00))          # R 450.00
print(categorise_transaction(-250)) # small

from datetime import date, datetime

today = date.today()
print(f"Report date: {today}")  # Report date: 2026-07-20

tx_time = datetime.now()
print(tx_time.strftime("%Y-%m-%d %H:%M:%S"))  # 2026-07-20 14:35:22

"""
fintrust_utils.py
Shared utilities for FinTrust Bank data processing scripts.
"""

from datetime import date
import math


# --- Formatting ---

def format_rand(amount):
    """Return amount formatted as South African Rand string."""
    return f"R {amount:,.2f}"


def mask_id_number(id_number):
    """Mask middle 6 digits of a 13-digit SA ID number."""
    s = str(id_number)
    if len(s) != 13:
        return s
    return s[:6] + "******" + s[-1]


# --- Validation ---

def validate_id_number(id_number):
    """Return True if id_number is a valid 13-digit numeric SA ID."""
    s = str(id_number)
    return len(s) == 13 and s.isdigit()


def validate_account_type(account_type):
    """Return True if account_type is one of the valid FinTrust types."""
    return account_type in ("cheque", "savings", "credit")


# --- Calculations ---

def calculate_simple_interest(principal, annual_rate, months):
    """Return simple interest amount for given principal, rate, and months."""
    return principal * annual_rate * (months / 12)


def calculate_monthly_fee(account_type):
    """Return monthly admin fee for a given account type."""
    fees = {"savings": 0.00, "cheque": 65.00, "credit": 120.00}
    return fees.get(account_type, 0.00)


def categorise_transaction(amount):
    """Return 'small', 'medium', or 'large' based on absolute transaction amount."""
    abs_amount = abs(amount)
    if abs_amount < 500:
        return "small"
    elif abs_amount < 5000:
        return "medium"
    return "large"


def summarise_transactions(amounts):
    """
    Return (total_deposits, total_withdrawals, net) from a list of amounts.
    Positive values are deposits, negative are withdrawals.
    """
    deposits = sum(a for a in amounts if a > 0)
    withdrawals = sum(a for a in amounts if a < 0)
    return deposits, withdrawals, deposits + withdrawals


# --- Report helpers ---

def generate_report_header(customer_name, account_id):
    """Return a formatted report header string."""
    today = date.today().strftime("%d %B %Y")
    return (
        f"FinTrust Bank — Account Statement\n"
        f"Customer: {customer_name}\n"
        f"Account: {account_id}\n"
        f"Date: {today}\n"
        f"{'-' * 40}"
    )