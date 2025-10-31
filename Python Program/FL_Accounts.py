import pandas as pd

# Import CSV files (equivalent to proc import)
FL_Accounts = pd.read_csv("c:/users/daryl/FL_Accounts.csv")
FL_Payments_9_2025 = pd.read_csv("c:/users/daryl/FL_Payments_9_2025.csv")

# Sort by customer_number (equivalent to proc sort)
FL_Accounts = FL_Accounts.sort_values('customer_number')
FL_Payments_9_2025 = FL_Payments_9_2025.sort_values('customer_number')

# Left join the datasets (equivalent to proc sql)
Accounts = FL_Accounts.merge(FL_Payments_9_2025, 
                            on='customer_number', 
                            how='left')

# Data step operations
FL_Accounts = Accounts.copy()
FL_Accounts['last_payment'] = FL_Accounts['payment_date']
FL_Accounts['account_balance'] = FL_Accounts['account_balance'] - FL_Accounts['payment_amount']

# Drop columns (equivalent to drop statement)
FL_Accounts = FL_Accounts.drop(columns=['payment_date', 'payment_amount'])

# Print the data (equivalent to proc print)
print(FL_Accounts)

# Export to CSV (equivalent to proc export)
FL_Accounts.to_csv("c:/users/daryl/FL_Accounts.csv", index=False)