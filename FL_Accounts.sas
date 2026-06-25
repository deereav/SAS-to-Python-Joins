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
proc sql;
create table Accounts as
select *
from FL_Accounts as a
left join FL_Payments_9_2025 as b
on a.customer_number = b.customer_number;
quit;
Data FL_Accounts;
Set  Accounts;
last_payment = payment_date;
account_balance= account_balance - payment_amount;
drop payment_date payment_amount;
run;

proc print data=FL_Accounts;
run;
proc export data=FL_Accounts
DBMS=csv
OUTFILE="/home/u39806166/FL_Accounts.csv"
replace;
run;
