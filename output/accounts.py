from datetime import datetime
from typing import Optional, List, Dict

def get_share_price(symbol: str) -> float:
    """
    Returns current price for given share symbol.
    Test implementation returns fixed prices for 'AAPL', 'TSLA', 'GOOGL'.
    """
    prices = {
        "AAPL": 150.0,
        "TSLA": 700.0,
        "GOOGL": 2700.0,
    }
    if symbol not in prices:
        raise ValueError(f"Invalid or unsupported symbol '{symbol}'.")
    return prices[symbol]

class Transaction:
    def __init__(self, timestamp: datetime, type: str, amount: float,
                 symbol: Optional[str] = None, quantity: Optional[int] = None):
        self.timestamp = timestamp
        self.type = type
        self.amount = amount
        self.symbol = symbol
        self.quantity = quantity

    def __repr__(self):
        return (f"Transaction(timestamp={self.timestamp!r}, type={self.type!r}, "
                f"amount={self.amount!r}, symbol={self.symbol!r}, quantity={self.quantity!r})")

class Account:
    def __init__(self) -> None:
        self.initial_deposit: Optional[float] = None
        self.cash_balance: float = 0.0
        self.holdings: Dict[str, int] = {}
        self.transactions: List[Transaction] = []

    def create_account(self, deposit_amount: float) -> None:
        if self.initial_deposit is not None:
            raise ValueError("Account already initialized.")
        if deposit_amount <= 0:
            raise ValueError("Initial deposit amount must be greater than zero.")
        self.initial_deposit = deposit_amount
        self.cash_balance = deposit_amount
        self._record_transaction("deposit", deposit_amount, None, None)

    def deposit(self, amount: float) -> None:
        self._ensure_account_initialized()
        if amount <= 0:
            raise ValueError("Deposit amount must be greater than zero.")
        self.cash_balance += amount
        self._record_transaction("deposit", amount, None, None)

    def withdraw(self, amount: float) -> None:
        self._ensure_account_initialized()
        if amount <= 0:
            raise ValueError("Withdrawal amount must be greater than zero.")
        if self.cash_balance - amount < 0:
            raise ValueError("Insufficient cash balance for withdrawal.")
        self.cash_balance -= amount
        self._record_transaction("withdrawal", amount, None, None)

    def buy(self, symbol: str, quantity: int) -> None:
        self._ensure_account_initialized()
        if quantity <= 0:
            raise ValueError("Quantity to buy must be greater than zero.")
        try:
            price = get_share_price(symbol)
        except ValueError:
            raise ValueError(f"Invalid or unsupported symbol '{symbol}'.")
        total_cost = price * quantity
        if self.cash_balance < total_cost:
            raise ValueError("Insufficient cash balance to buy shares.")
        self.cash_balance -= total_cost
        self.holdings[symbol] = self.holdings.get(symbol, 0) + quantity
        self._record_transaction("buy", total_cost, symbol, quantity)

    def sell(self, symbol: str, quantity: int) -> None:
        self._ensure_account_initialized()
        if quantity <= 0:
            raise ValueError("Quantity to sell must be greater than zero.")
        shares_held = self.holdings.get(symbol, 0)
        if shares_held < quantity:
            raise ValueError("Insufficient shares to sell.")
        try:
            price = get_share_price(symbol)
        except ValueError:
            raise ValueError(f"Invalid or unsupported symbol '{symbol}'.")
        proceeds = price * quantity
        self.cash_balance += proceeds
        new_quantity = shares_held - quantity
        if new_quantity > 0:
            self.holdings[symbol] = new_quantity
        else:
            del self.holdings[symbol]
        self._record_transaction("sell", proceeds, symbol, quantity)

    def get_portfolio_value(self) -> float:
        if self.initial_deposit is None:
            return 0.0
        total_value = self.cash_balance
        for symbol, qty in self.holdings.items():
            try:
                price = get_share_price(symbol)
            except ValueError:
                price = 0.0
            total_value += price * qty
        return total_value

    def get_profit_loss(self) -> float:
        if self.initial_deposit is None:
            return 0.0
        total_value = self.get_portfolio_value()
        return total_value - self.initial_deposit

    def get_holdings(self) -> Dict[str, int]:
        if self.initial_deposit is None:
            return {}
        return dict(self.holdings)

    def get_transactions(self) -> List[Transaction]:
        return list(self.transactions)

    def _ensure_account_initialized(self) -> None:
        if self.initial_deposit is None:
            raise ValueError("Account not initialized. Please create account first.")

    def _record_transaction(self, type: str, amount: float,
                            symbol: Optional[str], quantity: Optional[int]) -> None:
        transaction = Transaction(datetime.utcnow(), type, amount, symbol, quantity)
        self.transactions.append(transaction)