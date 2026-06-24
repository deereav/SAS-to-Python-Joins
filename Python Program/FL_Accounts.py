"""Apply monthly payments to customer account balances.

Left-joins payments to accounts so every customer is preserved.
Updates account_balance and last_payment only for customers who paid this month.
"""

from pathlib import Path
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "data"

# Load inputs
accounts = pd.read_csv(DATA / "FL_Accounts.csv")
payments = pd.read_csv(DATA / "FL_Payments_9_2025.csv")

# Left join keeps customers who didn't pay this month
out = accounts.merge(payments, on="customer_number", how="left")

# No payment -> NaN; treat as zero so the balance isn't wiped out
out["payment_amount"] = out["payment_amount"].fillna(0)
out["account_balance"] -= out["payment_amount"]

# Update last_payment only when a new payment exists; otherwise keep the prior value
out["last_payment"] = out["payment_date"].fillna(out["last_payment"])

# Drop the join-only columns
out = out.drop(columns=["payment_amount", "payment_date"])

# Write to a NEW file — never overwrite the input
out.to_csv(DATA / "FL_Accounts_python_out.csv", index=False)
print(out)
