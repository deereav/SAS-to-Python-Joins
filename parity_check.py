"""Verify SAS and Python outputs match row-for-row."""

from pathlib import Path
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "data"

def load(name):
    return (pd.read_csv(DATA / name)
              .sort_values("customer_number")
              .reset_index(drop=True))

sas_out = load("FL_Accounts_sas_out.csv")
py_out  = load("FL_Accounts_python_out.csv")

# check_dtype=False: SAS CSV export sometimes promotes ints to floats
pd.testing.assert_frame_equal(sas_out, py_out, check_dtype=False)
print(f"Parity check passed: {len(sas_out)} rows match.")
