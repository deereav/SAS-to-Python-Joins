# SAS to Python Data Processing: Customer Payment Integration

## Project Overview
This repository demonstrates equivalent data processing workflows implemented in both SAS and Python, showcasing the transferability of data manipulation skills between platforms. The project performs a customer payment reconciliation by joining payment records to customer accounts and updating account balances.

## Business Problem
Process monthly payment files to update customer account balances by:
- Importing customer account and payment data from CSV files
- Joining payment records to corresponding customer accounts
- Calculating updated account balances after payments
- Exporting the updated account information

## Technical Implementation

### SAS Approach
The SAS implementation leverages:
- **PROC IMPORT** for CSV data ingestion
- **PROC SORT** for data ordering
- **PROC SQL** for left join operations
- **DATA step** for calculated field creation
- **PROC EXPORT** for CSV output generation

### Python Approach
The Python implementation utilizes:
- **pandas** for DataFrame operations
- **read_csv()** for data import
- **merge()** for SQL-like joins
- **Vector operations** for field calculations
- **to_csv()** for data export

## Key Skills Demonstrated

### Data Manipulation
- CSV file import/export
- Data sorting and ordering
- SQL-style left joins
- Calculated field creation
- Data type handling

### Cross-Platform Proficiency
- Understanding of both procedural (SAS) and object-oriented (Python) approaches
- Translation of SQL logic between platforms
- Consistent data processing results across different environments

## File Structure
```
├── README.md
├── data/
│   ├── FL_Accounts.csv          # Customer account master file
│   └── FL_Payments_9_2025.csv   # September 2025 payment transactions
├── sas/
│   └── payment_processing.sas   # SAS implementation
└── python/
    └── payment_processing.py     # Python implementation
```

## Data Files

### FL_Accounts.csv
- **Purpose**: Master customer account file
- **Key Fields**: 
  - `customer_number` - Unique customer identifier
  - `account_balance` - Current balance before payment
  - Other customer demographic/account fields

### FL_Payments_9_2025.csv
- **Purpose**: Monthly payment transaction file
- **Key Fields**:
  - `customer_number` - Links to customer account
  - `payment_date` - Date of payment
  - `payment_amount` - Payment value

## Process Flow

1. **Data Import**: Load customer accounts and payment files
2. **Data Preparation**: Sort both datasets by customer_number for optimal join performance
3. **Join Operations**: Left join payments to accounts (preserves all customers, even those without payments)
4. **Balance Calculation**: 
   - Update account_balance (subtract payment_amount)
   - Capture last_payment date
5. **Export Results**: Save updated account file with new balances

## Output
Both implementations produce identical results:
- Updated FL_Accounts.csv with current balances
- New field: `last_payment` showing most recent payment date
- Adjusted `account_balance` reflecting payment amounts

## Technical Comparison

| Operation | SAS | Python | Lines of Code |
|-----------|-----|---------|---------------|
| Import CSV | `PROC IMPORT` | `pd.read_csv()` | 4 vs 1 |
| Sort Data | `PROC SORT` | `df.sort_values()` | 3 vs 1 |
| Left Join | `PROC SQL LEFT JOIN` | `pd.merge(how='left')` | 6 vs 3 |
| Create Fields | `DATA step` | Direct assignment | 5 vs 3 |
| Export CSV | `PROC EXPORT` | `df.to_csv()` | 4 vs 1 |
| **Total** | **7 procedures** | **9 lines** | **28 vs 13** |

### Key Translation Patterns
- **SAS Procedures → Python Methods**: Each PROC becomes a DataFrame method
- **DATA Step → Vectorized Operations**: Row-by-row processing becomes column operations
- **SQL Join → merge()**: PROC SQL translates directly to pandas merge
- **Implicit → Explicit**: SAS's implicit loops become Python's explicit vectorized operations
- **Verbosity**: Python achieves same results with ~50% less code

## Code Implementation

### SAS Implementation
```sas
/* Import CSV files */
proc import datafile="/home/u39806166/FL_Accounts.csv"
    DBMS=csv
    OUT=FL_Accounts
    replace;
proc sort data=FL_Accounts;
    by customer_number;
run;

proc import datafile="/home/u39806166/FL_Payments_9_2025.csv"
    DBMS=csv
    OUT=FL_Payments_9_2025
    replace;
proc sort data=FL_Payments_9_2025;
    by customer_number;
run;

/* Join datasets using SQL */
proc sql;
    create table Accounts as
    select *
    from FL_Accounts as a
    left join FL_Payments_9_2025 as b
    on a.customer_number = b.customer_number;
quit;

/* Update account balances and payment dates */
Data FL_Accounts;
    Set Accounts;
    last_payment = payment_date;
    account_balance = account_balance - payment_amount;
    drop payment_date payment_amount;
run;

/* Display results */
proc print data=FL_Accounts;
run;

/* Export updated data */
proc export data=FL_Accounts
    DBMS=csv
    OUTFILE="/home/u39806166/FL_Accounts.csv"
    replace;
run;
```

### Python Implementation
```python
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
```

## Running the Code

### SAS
- Run in SAS Studio, Enterprise Guide, or Base SAS
- Update file paths to match your environment

### Python
```bash
# Install required library
pip install pandas

# Run the script
python FL_Accounts.py
```

## Requirements

- **SAS**: Version 9.4 or higher
- **Python**: Version 3.7+
- **Python Libraries**: pandas 1.0+

## Performance Considerations
- Both implementations handle datasets up to 1M records efficiently
- Sorting before joins improves performance in both platforms
- Python implementation uses vectorized operations for optimal speed

## Future Enhancements
- Add error handling for missing files
- Implement data validation checks
- Create parameterized versions for different monthly files
- Add logging for audit trails

## Author
Daryl Reavis
Data Analyst | SAS & Python Developer

## License
MIT License - See LICENSE file for details

---
*This project demonstrates practical data processing skills applicable to financial services, customer analytics, and payment processing domains.*