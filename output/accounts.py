"""
accounts.py

A module implementing a simple account management system for a trading simulation platform.

Primary class:
- Account: Represents a user's trading account, managing funds, share transactions, and portfolio valuation.

Other components:
- get_share_price(symbol: str) -> float: Provides current share prices (test implementation with fixed data).
- Transaction: Internal data structure to represent a single transaction (buy/sell/deposit/withdraw).

Design focuses on:
- Clear class and method signatures for ease of testing.
- Robust validation to prevent invalid operations.
- Easy integration with UIs or other modules.
"""

from typing import List, Dict, Union
from dataclasses import dataclass
from datetime import datetime


def get_share_price(symbol: str) -> float:
    """
    Test implementation returning fixed share prices for known symbols.
    In a real system, this would interface with a pricing service.

    Args:
        symbol (str): Stock symbol.

    Returns:
        float: Current price of the share.

    Raises:
        ValueError: If the symbol is unknown.
    """
    prices = {
        'AAPL': 150.0,
        'TSLA': 700.0,
        'GOOGL': 2800.0,
    }
    if symbol not in prices:
        raise ValueError(f"Unknown share symbol: {symbol}")
    return prices[symbol]


@dataclass(frozen=True)
class Transaction:
    """
    Represents a financial or share transaction in the account.

    Attributes:
        timestamp (datetime): When the transaction occurred.
        type (str): One of {'deposit', 'withdrawal', 'buy', 'sell'}.
        amount (float): Amount of money involved (for deposits/withdrawals).
        symbol (Union[str, None]): Stock symbol (for buys/sells), None otherwise.
        quantity (Union[int, None]): Number of shares bought or sold, None for deposit/withdrawal.
        price_per_share (Union[float, None]): Share price at transaction time, None for deposit/withdrawal.
    """
    timestamp: datetime
    type: str
    amount: float = 0.0
    symbol: Union[str, None] = None
    quantity: Union[int, None] = None
    price_per_share: Union[float, None] = None


class Account:
    """
    Represents a user's trading account that tracks deposits, withdrawals,
    share transactions, portfolio valuation, and profit/loss.

    Responsibilities:
    - Manage cash balance and stock holdings.
    - Record all transactions.
    - Enforce rules preventing overdrawing or invalid trades.
    - Provide portfolio value and profit/loss reports.
    """

    def __init__(self) -> None:
        """
        Initialize a new Account.

        Starts with zero cash balance and no holdings.
        Initializes empty transaction history.
        """
        self._cash_balance: float = 0.0
        self._holdings: Dict[str, int] = {}  # symbol -> share count
        self._transactions: List[Transaction] = []
        self._initial_deposit: float = 0.0

    def create_account(self, initial_deposit: float) -> None:
        """
        Create account with an initial deposit.

        Args:
            initial_deposit (float): Starting cash added to the account; must be > 0.

        Raises:
            ValueError: If initial_deposit <= 0 or account already created.
        """
        if self._initial_deposit > 0:
            raise ValueError("Account already created with initial deposit.")
        if initial_deposit <= 0:
            raise ValueError("Initial deposit must be greater than zero.")

        self._cash_balance = initial_deposit
        self._initial_deposit = initial_deposit
        self._transactions.append(
            Transaction(
                timestamp=datetime.now(),
                type="deposit",
                amount=initial_deposit
            )
        )

    def deposit(self, amount: float) -> None:
        """
        Deposit additional funds into the account.

        Args:
            amount (float): Amount to deposit > 0.

        Raises:
            ValueError: If amount <= 0.
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be greater than zero.")
        self._cash_balance += amount
        self._transactions.append(
            Transaction(
                timestamp=datetime.now(),
                type="deposit",
                amount=amount
            )
        )

    def withdraw(self, amount: float) -> None:
        """
        Withdraw funds from the account.

        Args:
            amount (float): Amount to withdraw > 0.

        Raises:
            ValueError: If amount <= 0 or insufficient cash balance.
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be greater than zero.")
        if amount > self._cash_balance:
            raise ValueError("Insufficient funds for withdrawal.")
        self._cash_balance -= amount
        self._transactions.append(
            Transaction(
                timestamp=datetime.now(),
                type="withdrawal",
                amount=amount
            )
        )

    def buy(self, symbol: str, quantity: int) -> None:
        """
        Record purchase of shares.

        Args:
            symbol (str): Stock symbol to buy.
            quantity (int): Number of shares to buy (> 0).

        Raises:
            ValueError: If symbol unknown, quantity not positive,
                        or insufficient funds to cover purchase.
        """
        if quantity <= 0:
            raise ValueError("Quantity to buy must be greater than zero.")
        share_price = get_share_price(symbol)
        total_cost = share_price * quantity
        if total_cost > self._cash_balance:
            raise ValueError("Insufficient funds to buy shares.")
        # Deduct cost
        self._cash_balance -= total_cost
        # Update holdings
        self._holdings[symbol] = self._holdings.get(symbol, 0) + quantity
        # Record transaction
        self._transactions.append(
            Transaction(
                timestamp=datetime.now(),
                type="buy",
                symbol=symbol,
                quantity=quantity,
                price_per_share=share_price
            )
        )

    def sell(self, symbol: str, quantity: int) -> None:
        """
        Record sale of shares.

        Args:
            symbol (str): Stock symbol to sell.
            quantity (int): Number of shares to sell (> 0).

        Raises:
            ValueError: If symbol unknown, quantity not positive,
                        or insufficient shares held to sell.
        """
        if quantity <= 0:
            raise ValueError("Quantity to sell must be greater than zero.")
        current_quantity = self._holdings.get(symbol, 0)
        if quantity > current_quantity:
            raise ValueError("Insufficient shares held to sell.")
        share_price = get_share_price(symbol)
        total_proceeds = share_price * quantity
        # Update holdings
        new_quantity = current_quantity - quantity
        if new_quantity == 0:
            del self._holdings[symbol]
        else:
            self._holdings[symbol] = new_quantity
        # Add proceeds to cash balance
        self._cash_balance += total_proceeds
        # Record transaction
        self._transactions.append(
            Transaction(
                timestamp=datetime.now(),
                type="sell",
                symbol=symbol,
                quantity=quantity,
                price_per_share=share_price
            )
        )

    def get_cash_balance(self) -> float:
        """
        Get current cash balance.

        Returns:
            float: Current cash available in account.
        """
        return self._cash_balance

    def get_holdings(self) -> Dict[str, int]:
        """
        Get current stock holdings.

        Returns:
            Dict[str, int]: Mapping symbol -> number of shares held.
        """
        # Return a copy to prevent external mutation
        return dict(self._holdings)

    def get_portfolio_value(self) -> float:
        """
        Calculate total portfolio value (cash + market value of shares).

        Returns:
            float: Total portfolio value based on current share prices.
        """
        total_value = self._cash_balance
        for symbol, quantity in self._holdings.items():
            share_price = get_share_price(symbol)
            total_value += share_price * quantity
        return total_value

    def get_profit_loss(self) -> float:
        """
        Calculate profit or loss relative to the initial deposit.

        Returns:
            float: Profit (positive) or loss (negative)
        """
        current_value = self.get_portfolio_value()
        return current_value - self._initial_deposit

    def list_transactions(self) -> List[Transaction]:
        """
        Get full history of transactions.

        Returns:
            List[Transaction]: Ordered list of all transactions by timestamp.
        """
        # Return a copy to prevent external mutation
        return list(self._transactions)