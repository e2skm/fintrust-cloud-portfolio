class BankingError(Exception):
    """Base class for all FinTrust banking errors."""
    pass

class InsufficientFundsError(BankingError):
    """Raised when a transaction exceeds available balance."""

    def __init__(self, account_id, requested, available):
        self.account_id = account_id
        self.requested = requested
        self.available = available
        self.shortfall = requested - available
        message = (
            f"Account {account_id}: requested R{requested:.2f} "
            f"but only R{available:.2f} available "
            f"(shortfall: R{self.shortfall:.2f})"
        )
        super().__init__(message)


# Raise it
def withdraw(account_id, amount, balance):
    if amount > balance:
        raise InsufficientFundsError(account_id, amount, balance)
    return balance - amount


# Catch it with full context
try:
    new_balance = withdraw("FT-001234", 5000.00, 3200.50)
except InsufficientFundsError as e:
    print(f"Transaction declined: {e}")
    print(f"Shortfall: R{e.shortfall:.2f}")
    # Can access e.account_id, e.requested, e.available directly

class TransactionError(BankingError):
    """Any error during transaction processing."""
    def __init__(self, transaction_id, message):
        self.transaction_id = transaction_id
        super().__init__(f"[TXN:{transaction_id}] {message}")


class InsufficientFundsError(TransactionError):
    """Balance too low to complete the transaction."""
    def __init__(self, transaction_id, account_id, requested, available):
        self.account_id = account_id
        self.requested = requested
        self.available = available
        self.shortfall = requested - available
        super().__init__(
            transaction_id,
            f"Account {account_id} short by R{self.shortfall:.2f}"
        )


class AccountFrozenError(TransactionError):
    """Account is frozen due to compliance hold."""
    def __init__(self, transaction_id, account_id, reason):
        self.account_id = account_id
        self.reason = reason
        super().__init__(transaction_id, f"Account {account_id} frozen: {reason}")


class DailyLimitExceededError(TransactionError):
    """Transaction would breach the daily transfer limit."""
    def __init__(self, transaction_id, account_id, limit, already_used, requested):
        self.account_id = account_id
        self.limit = limit
        self.already_used = already_used
        self.requested = requested
        remaining = limit - already_used
        super().__init__(
            transaction_id,
            f"Daily limit R{limit:.2f}: used R{already_used:.2f}, "
            f"remaining R{remaining:.2f}, requested R{requested:.2f}"
        )

# test_custom_exceptions.py

def test_insufficient_funds():
    try:
        raise InsufficientFundsError(
            transaction_id="TXN001",
            account_id="ACC1001",
            requested=5000.00,
            available=3200.50
        )
    except InsufficientFundsError as e:
        print("=== InsufficientFundsError Test ===")
        print(f"Message      : {e}")
        print(f"Transaction  : {e.transaction_id}")
        print(f"Account      : {e.account_id}")
        print(f"Requested    : {e.requested}")
        print(f"Available    : {e.available}")
        print(f"Shortfall    : {e.shortfall}")
        print()


def test_account_frozen():
    try:
        raise AccountFrozenError(
            transaction_id="TXN002",
            account_id="ACC1002",
            reason="Compliance Hold"
        )
    except AccountFrozenError as e:
        print("=== AccountFrozenError Test ===")
        print(f"Message      : {e}")
        print(f"Transaction  : {e.transaction_id}")
        print(f"Account      : {e.account_id}")
        print(f"Reason       : {e.reason}")
        print()


def test_daily_limit_exceeded():
    try:
        raise DailyLimitExceededError(
            transaction_id="TXN003",
            account_id="ACC1003",
            limit=10000.00,
            already_used=8500.00,
            requested=3000.00
        )
    except DailyLimitExceededError as e:
        print("=== DailyLimitExceededError Test ===")
        print(f"Message      : {e}")
        print(f"Transaction  : {e.transaction_id}")
        print(f"Account      : {e.account_id}")
        print(f"Limit        : {e.limit}")
        print(f"Used         : {e.already_used}")
        print(f"Requested    : {e.requested}")
        print()


if __name__ == "__main__":
    test_insufficient_funds()
    test_account_frozen()
    test_daily_limit_exceeded()

try:
    raise InsufficientFundsError(
        "TXN004",
        "ACC1004",
        5000.00,
        1000.00
    )

except Exception as e:
    print("Caught as Exception:", type(e).__name__)

except BankingError as e:
    print("Caught as BankingError:", type(e).__name__)