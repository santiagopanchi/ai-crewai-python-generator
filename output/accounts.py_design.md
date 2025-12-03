```markdown
# Backend Design for `accounts.py` Module

## Overview
The `accounts.py` module provides a backend design for a simple account management system used in a trading simulation platform. The primary class is `Account`, which encapsulates user account state and behaviors such as depositing, withdrawing, buying, and selling shares, along with reporting portfolio value, profit/loss, holdings, and transaction history.

This design prioritizes:
- **Testability:** Clear method boundaries, easy-to-assert state changes, and no external side effects except the `get_share_price` function.
- **Extensibility:** Future methods or account types can be added; encapsulated transactions enable adding additional transaction kinds or audit trails.
- **Integration:** Simple method signatures with return values and exceptions for invalid operations facilitate integration with UI or other layers.

---

## Module Components

### 1. Function: `get_share_price(symbol: str) -> float`
- **Responsibility:** Return the current price of a stock share by its symbol.
- **Notes:**  
  - Provided as a standalone function, assumed accessible by the `Account` class.
  - Includes a test implementation returning fixed prices for `"AAPL"`, `"TSLA"`, and `"GOOGL"`.
- **Signature:**  
  ```python
  def get_share_price(symbol: str) -> float
  ```
- **Example behavior:**  
  ```python
  get_share_price("AAPL")  # returns fixed price, e.g., 150.0
  ```

---

### 2. Class: `Transaction`
- **Responsibility:** Represent a single transaction record for the Account.
- **Attributes:**
  - `timestamp: datetime` — time when the transaction occurred
  - `type: str` — `"deposit"`, `"withdrawal"`, `"buy"`, or `"sell"`
  - `amount: float` — money amount for deposits/withdrawals or total cost for buy/sell
  - `symbol: Optional[str]` — stock symbol for buy/sell transactions; None otherwise
  - `quantity: Optional[int]` — quantity of shares bought/sold; None otherwise
- **Purpose:** Decouples transaction data from business logic, allowing history listing and auditing.
- **Signature:**  
  ```python
  class Transaction:
      def __init__(self, timestamp: datetime, type: str, amount: float,
                   symbol: Optional[str] = None, quantity: Optional[int] = None):
          ...
  ```

---

### 3. Class: `Account`
The central class encapsulating all account information and trading behavior.

#### Attributes:
- `initial_deposit: float`
- `cash_balance: float` — available cash for trades and withdrawals
- `holdings: Dict[str, int]` — shares held keyed by symbol
- `transactions: List[Transaction]` — ordered list of transaction records
- **Design:**  
  Hold granular state to easily calculate portfolio values and enforce constraints.

#### Constructor:
```python
def __init__(self)
```
- Initializes empty account (zero balances and no transactions).

#### Methods:

1. **create_account(deposit_amount: float) -> None**
   - Initialize account by making the first deposit.
   - Sets `initial_deposit` and `cash_balance` to `deposit_amount`.
   - Records a deposit transaction.
   - Raises ValueError if deposit_amount <= 0 or if account already initialized.
  
2. **deposit(amount: float) -> None**
   - Adds funds to `cash_balance`.
   - Records a deposit transaction.
   - Raises ValueError if amount <= 0 or account not initialized.

3. **withdraw(amount: float) -> None**
   - Decreases `cash_balance` by amount.
   - Records a withdrawal transaction.
   - Raises ValueError if amount <= 0, account not initialized, or withdrawal results in negative balance.

4. **buy(symbol: str, quantity: int) -> None**
   - Purchase shares of `symbol` at current price `get_share_price(symbol)`.
   - Calculates total_cost = price * quantity.
   - Checks if `cash_balance` >= total_cost before proceeding.
   - Deducts total_cost from `cash_balance`.
   - Updates `holdings` by adding quantity.
   - Records a buy transaction.
   - Raises ValueError if quantity <= 0, insufficient funds, invalid symbol, or account not initialized.

5. **sell(symbol: str, quantity: int) -> None**
   - Sell shares of `symbol` at current price.
   - Checks if holdings for `symbol` >= quantity.
   - Calculates proceeds = price * quantity.
   - Adds proceeds to `cash_balance`.
   - Updates `holdings` by reducing quantity.
   - Records a sell transaction.
   - Raises ValueError if quantity <= 0, insufficient shares, invalid symbol, or account not initialized.

6. **get_portfolio_value() -> float**
   - Returns total current value of: `cash_balance` + sum for each symbol (price * quantity held).
   - Uses `get_share_price` to retrieve live prices.
   - Returns 0 if account uninitialized.

7. **get_profit_loss() -> float**
   - Returns current portfolio total value minus `initial_deposit`.
   - Positive if profit, negative if loss, zero if break-even or uninitialized.

8. **get_holdings() -> Dict[str, int]**
   - Returns a copy of current holdings dictionary (symbol → quantity).
   - Empty dict if no holdings or uninitialized.

9. **get_transactions() -> List[Transaction]**
   - Returns ordered list of all transactions made on the account.
   - Empty list if no transactions.

---

## Summary of Interactions

- User creates account with an initial deposit (creates baseline for profit/loss).
- User deposits/withdraws cash that updates `cash_balance` and records transactions.
- User buys shares when they have enough cash, updating holdings and cash.
- User sells shares only if they have sufficient quantity, cash updated accordingly.
- User queries portfolio value and profit/loss dynamically using live prices.
- Transaction history enables audit and UI display.
- All state changes generate transactions for consistent state tracking.
- `get_share_price` external dependency mocked for testing and fixed prices.

---

## Example Module Skeleton (Signatures Only)

```python
from datetime import datetime
from typing import Optional, List, Dict

def get_share_price(symbol: str) -> float:
    """
    Returns current price for given share symbol.
    Test implementation returns fixed prices for 'AAPL', 'TSLA', 'GOOGL'.
    """
    ...

class Transaction:
    def __init__(self, timestamp: datetime, type: str, amount: float,
                 symbol: Optional[str] = None, quantity: Optional[int] = None):
        ...

class Account:
    def __init__(self) -> None:
        ...

    def create_account(self, deposit_amount: float) -> None:
        """
        Initialize account with initial deposit.
        """

    def deposit(self, amount: float) -> None:
        """
        Deposit funds into account.
        """

    def withdraw(self, amount: float) -> None:
        """
        Withdraw funds from account if sufficient balance.
        """

    def buy(self, symbol: str, quantity: int) -> None:
        """
        Buy shares of symbol if enough cash balance.
        """

    def sell(self, symbol: str, quantity: int) -> None:
        """
        Sell shares of symbol if holdings sufficient.
        """

    def get_portfolio_value(self) -> float:
        """
        Compute total portfolio value: cash + holdings.
        """

    def get_profit_loss(self) -> float:
        """
        Compute profit/loss from initial deposit.
        """

    def get_holdings(self) -> Dict[str, int]:
        """
        Get current holdings dictionary.
        """

    def get_transactions(self) -> List[Transaction]:
        """
        Return list of all transactions.
        """
```

---

This design provides a clear, self-contained Python module layout focusing on correctness, clarity, testability, and ease of integration with any frontend or manual testing harness.
```