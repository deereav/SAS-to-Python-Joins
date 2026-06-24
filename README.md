# SAS to Python: Customer Payment Join

A side-by-side SAS and Python implementation of the same payment-processing
job, plus an automated parity check that proves the two outputs match.

## Why this exists

Most SAS-to-Python migrations don't fail on the obvious code — they fail on
edge cases where the two languages handle missing values, types, or sort
order differently. This repo shows the full loop: translate the code, run
both versions, and verify the outputs are identical.

## The job

Apply a monthly payment file to a customer account file:

1. Left-join payments to accounts on `customer_number`.
2. Subtract `payment_amount` from `account_balance`.
3. Update `last_payment` with the new payment date.
4. Write the updated accounts to a new file.

## Repo layout

    data/         Input CSVs and generated outputs
    sas/          SAS implementation (fl_account.txt)
    python/       Python implementation (fl_accounts.py)
    validation/   Parity check comparing both outputs

## Data files

### FL_Accounts.csv — master customer account file
Columns: `first_name`, `last_name`, `address`, `city`, `state`, `zip_code`,
`customer_number`, `account_balance`, `last_payment`

### FL_Payments_9_2025.csv — monthly payment transactions
Columns: `customer_number`, `payment_amount`, `payment_date`

## Run it

    # Python
    python python/fl_accounts.py

    # SAS (SAS Studio or Base SAS, with working directory at repo root)
    %include "sas/fl_account.txt";

    # Verify the two outputs match
    python validation/parity_check.py

## The gotcha this repo highlights

A naive left join leaves `payment_amount` missing (`NaN` in pandas, `.` in
SAS) for customers who didn't pay this month. Subtracting that from
`account_balance` silently destroys the balance — the job runs without
errors, but the data is wrong. The same problem hits `last_payment`: a naive
overwrite wipes out the customer's prior payment date.

- **Python fix:** `df["payment_amount"].fillna(0)` before the subtraction,
  and `df["payment_date"].fillna(df["last_payment"])` for the date.
- **SAS fix:** `coalesce(b.payment_amount, 0)` and
  `coalesce(b.payment_date, a.last_payment)` inside the `PROC SQL` select.

This is the kind of difference an automated parity check catches early —
before it ships to production and a regulator finds it.

## SAS implementation

```sas
%let data_dir = ./data;

proc import datafile="&data_dir/FL_Accounts.csv"        dbms=csv out=fl_accounts replace; run;
proc import datafile="&data_dir/FL_Payments_9_2025.csv" dbms=csv out=fl_payments replace; run;

proc sql;
    create table fl_accounts_out as
    select a.first_name,
           a.last_name,
           a.address,
           a.city,
           a.state,
           a.zip_code,
           a.customer_number,
           a.account_balance - coalesce(b.payment_amount, 0)
               as account_balance format=12.2,
           coalesce(b.payment_date, a.last_payment)
               as last_payment format=yymmdd10.
    from fl_accounts as a
    left join fl_payments as b
      on a.customer_number = b.customer_number;
quit;

proc print data=fl_accounts_out; run;

proc export data=fl_accounts_out
    outfile="&data_dir/FL_Accounts_sas_out.csv" dbms=csv replace; run;
```

## Python implementation

```python
from pathlib import Path
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "data"

accounts = pd.read_csv(DATA / "FL_Accounts.csv")
payments = pd.read_csv(DATA / "FL_Payments_9_2025.csv")

out = accounts.merge(payments, on="customer_number", how="left")

out["payment_amount"] = out["payment_amount"].fillna(0)
out["account_balance"] -= out["payment_amount"]
out["last_payment"] = out["payment_date"].fillna(out["last_payment"])

out = out.drop(columns=["payment_amount", "payment_date"])
out.to_csv(DATA / "FL_Accounts_python_out.csv", index=False)
print(out)
```

## Translation patterns

| Operation     | SAS                       | Python                    |
|---------------|---------------------------|---------------------------|
| Import CSV    | `PROC IMPORT`             | `pd.read_csv()`           |
| Left join     | `PROC SQL LEFT JOIN`      | `df.merge(how='left')`    |
| Missing → 0   | `coalesce(x, 0)`          | `df['x'].fillna(0)`       |
| Calculated col| `select expr as name`     | `df['name'] = expr`       |
| Export CSV    | `PROC EXPORT`             | `df.to_csv()`             |

Key patterns:
- SAS procedures become DataFrame methods.
- SAS missing values (`.`) and pandas `NaN` propagate the same way through
  arithmetic — both need explicit handling, not just translation.
- `PROC SQL` translates almost line-for-line to pandas `merge`.

## Requirements

- SAS 9.4 or higher (SAS Studio, SAS OnDemand, or Base SAS)
- Python 3.9+, pandas 1.0+

## Future enhancements

- Error handling for missing input files
- Logging for audit trails
- Parameterized version for any month's payment file

## Author

Daryl Reavis — SAS programmer focused on legacy SAS maintenance and
SAS-to-Python migration with output parity validation.

## License

MIT License — see LICENSE file for details.
