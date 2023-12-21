## **README.md**

### **Description**

This Python code is a simple application for managing financial accounts, including credit accounts, checking accounts, and savings accounts. It allows you to record expenses, receipts, export/import statements, and query invoices.

### **Requirements**
- Required libraries: numpy, matplotlib, pandas, openpyxl

### **Code Structure**
The code is divided into three main classes:

- Account: Base class that stores common information for all accounts (account holder's name, bank name, etc.).

- Credit (Account): Class representing a credit account. Allows recording expenses, calculating invoices, and exporting/importing invoices in CSV format.

- Checking (Account): Class representing a checking account. Allows recording receipts, expenses, and exporting/importing statements in CSV format.

- Savings (Account): Class representing a savings account. Allows displaying a summary of the interest.

### **Features**
**Account Class**
- Method summary(): Displays a summary of the account information.
**Credit Class**
- Method summary(): Displays a summary of the credit account.
- Method expense(date, descr, value, installment=1): Records an expense in the credit account, allowing installment payments.
- Method export_invoice(path=None): Exports the credit account invoice to a CSV file.
- Method query_invoice(path=None): Queries the credit account invoice from a CSV file.
**Checking Class**
- Method receipt(date, desc, value): Records a receipt in the checking account.
- Method expense(date, desc, value): Records an expense in the checking account.
- Method export_statement(path=None): Exports the checking account statement to a CSV file.
- Method query_statement(path=None): Queries the checking account statement from a CSV file.
**Savings Class**
- Method summary(): Displays a summary of the savings account.

### **Usage Examples**

```python
# Example of using a credit account (NuBank)
nu_credit = Credit('Rafael', 'NuBank', 5000, '18/12/2023', '26/12/2023')
nu_credit.expense('10/12/2023', 'Christmas Shopping', 300)
nu_credit.export_invoice()
nu_credit.query_invoice()

# Example of using a checking account (NuBank)
nu_checking = Checking('Rafael', 'NuBank')
nu_checking.receipt('1/1/2024', 'Pix', 500)
nu_checking.expense('2/1/2024', 'Bakery', 30)
nu_checking.export_statement()
nu_checking.query_statement()

# Example of using a savings account
savings_account = Savings('João', 1000, 0.5)
savings_account.summary()
```
### **Authors**
Gabriel Tomé Silveira
Rafael Godoi Cutait 
Tainá Santos
