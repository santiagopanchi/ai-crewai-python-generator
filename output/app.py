import gradio as gr
from accounts import Account, get_share_price
from datetime import datetime

account = Account()

def create_account_ui(initial_deposit):
    try:
        account.create_account(initial_deposit)
        return f"Account created with initial deposit: ${initial_deposit:.2f}"
    except Exception as e:
        return str(e)

def deposit_ui(amount):
    try:
        account.deposit(amount)
        return f"Deposited ${amount:.2f} successfully."
    except Exception as e:
        return str(e)

def withdraw_ui(amount):
    try:
        account.withdraw(amount)
        return f"Withdrew ${amount:.2f} successfully."
    except Exception as e:
        return str(e)

def buy_shares_ui(symbol, quantity):
    symbol = symbol.upper()
    try:
        # check valid symbol before buy to display better errors
        _ = get_share_price(symbol)
        account.buy(symbol, quantity)
        return f"Bought {quantity} shares of {symbol}."
    except Exception as e:
        return str(e)

def sell_shares_ui(symbol, quantity):
    symbol = symbol.upper()
    try:
        _ = get_share_price(symbol)
        account.sell(symbol, quantity)
        return f"Sold {quantity} shares of {symbol}."
    except Exception as e:
        return str(e)

def show_cash_balance_ui():
    cash = account.get_cash_balance()
    return f"Cash balance: ${cash:.2f}"

def show_holdings_ui():
    holdings = account.get_holdings()
    if not holdings:
        return "No holdings."
    lines = []
    for sym, qty in holdings.items():
        price = get_share_price(sym)
        value = price * qty
        lines.append(f"{sym}: {qty} shares @ ${price:.2f} = ${value:.2f}")
    return "\n".join(lines)

def show_portfolio_value_ui():
    value = account.get_portfolio_value()
    return f"Total portfolio value (cash + shares): ${value:.2f}"

def show_profit_loss_ui():
    pl = account.get_profit_loss()
    sign = "+" if pl >= 0 else "-"
    return f"Profit/Loss relative to initial deposit: {sign}${abs(pl):.2f}"

def list_transactions_ui():
    txs = account.list_transactions()
    if not txs:
        return "No transactions yet."
    lines = []
    for t in txs:
        ts = t.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        if t.type in ("deposit", "withdrawal"):
            lines.append(f"{ts} - {t.type.capitalize()}: ${t.amount:.2f}")
        elif t.type in ("buy", "sell"):
            lines.append(f"{ts} - {t.type.capitalize()} {t.quantity} shares of {t.symbol} @ ${t.price_per_share:.2f}")
    return "\n".join(lines)

with gr.Blocks() as demo:
    gr.Markdown("# Trading Account Simulator")
    with gr.Tab("Account Setup"):
        with gr.Row():
            initial_deposit = gr.Number(label="Initial Deposit ($)", value=1000, precision=2)
            create_btn = gr.Button("Create Account")
        create_out = gr.Textbox(label="Status", interactive=False)
        create_btn.click(create_account_ui, inputs=initial_deposit, outputs=create_out)

    with gr.Tab("Manage Cash"):
        with gr.Row():
            deposit_amount = gr.Number(label="Deposit Amount ($)", precision=2)
            deposit_btn = gr.Button("Deposit")
            withdraw_amount = gr.Number(label="Withdraw Amount ($)", precision=2)
            withdraw_btn = gr.Button("Withdraw")
        cash_status = gr.Textbox(label="Status", interactive=False)
        deposit_btn.click(deposit_ui, inputs=deposit_amount, outputs=cash_status)
        withdraw_btn.click(withdraw_ui, inputs=withdraw_amount, outputs=cash_status)
        show_cash_btn = gr.Button("Show Cash Balance")
        cash_balance_out = gr.Textbox(label="Cash Balance", interactive=False)
        show_cash_btn.click(show_cash_balance_ui, outputs=cash_balance_out)

    with gr.Tab("Trading"):
        with gr.Row():
            buy_symbol = gr.Textbox(label="Buy Symbol", value="AAPL", max_length=5)
            buy_quantity = gr.Number(label="Buy Quantity", value=1, precision=0, interactive=True)
            buy_btn = gr.Button("Buy")
        buy_status = gr.Textbox(label="Buy Status", interactive=False)
        buy_btn.click(buy_shares_ui, inputs=[buy_symbol, buy_quantity], outputs=buy_status)

        with gr.Row():
            sell_symbol = gr.Textbox(label="Sell Symbol", value="AAPL", max_length=5)
            sell_quantity = gr.Number(label="Sell Quantity", value=1, precision=0, interactive=True)
            sell_btn = gr.Button("Sell")
        sell_status = gr.Textbox(label="Sell Status", interactive=False)
        sell_btn.click(sell_shares_ui, inputs=[sell_symbol, sell_quantity], outputs=sell_status)

    with gr.Tab("Portfolio"):
        show_holdings_btn = gr.Button("Show Holdings")
        holdings_out = gr.Textbox(label="Current Holdings", interactive=False)
        show_holdings_btn.click(show_holdings_ui, outputs=holdings_out)

        show_value_btn = gr.Button("Show Portfolio Value")
        portfolio_value_out = gr.Textbox(label="Portfolio Value", interactive=False)
        show_value_btn.click(show_portfolio_value_ui, outputs=portfolio_value_out)

        show_pl_btn = gr.Button("Show Profit/Loss")
        pl_out = gr.Textbox(label="Profit/Loss", interactive=False)
        show_pl_btn.click(show_profit_loss_ui, outputs=pl_out)

    with gr.Tab("Transactions"):
        list_tx_btn = gr.Button("List Transactions")
        tx_out = gr.Textbox(label="Transaction History", interactive=False, lines=15)
        list_tx_btn.click(list_transactions_ui, outputs=tx_out)

if __name__ == "__main__":
    demo.launch()