# 🏦 Bank Management System — Project Output

**Project by:** Sanika Kadam  
**Language:** Python  
**Application type:** Menu-driven console application

---

## 1. Project Overview

The Bank Management System simulates basic banking services using Python. A customer can create an account, log in with a PIN, check balances, deposit or withdraw money, transfer funds, manage cards, apply for loans, and use locker services.

The program uses dictionaries to store account details and lists to maintain transaction histories while the application is running.

## 2. Main Menu

When the program starts, it displays a menu similar to this:

```text
============================================
------ BANK SYSTEM ------
============================================
1. Create Account
2. Login
3. Exit
Enter Your Choice:
```

## 3. Example Account Creation

The following is an **illustrative sample** of what the output may look like. The generated account number and values will vary each time.

```text
============================================
ACCOUNT CREATION
============================================
Enter Your Name: Sanika Kadam
Enter Your Gender: Female
Enter Date of Birth (DD/MM/YYYY): 15/05/2005
Enter Mobile Number (10 digits): 9876543210

Choose Account Type:
1. Current Account (min balance Rs.5000)
2. Savings Account (min balance Rs.1000)
Enter Your Choice: 2
Enter Initial Balance: 5000
Set a 4-digit PIN: ****

============================================
ACCOUNT CREATED SUCCESSFULLY
Account Holder : Sanika Kadam
Account Type   : Savings
Balance        : Rs.5000
Account Number : 123456789012
============================================
```

**Note:** The sample account number above is fictional. The program generates a random 12-digit account number, so your actual output will be different. The example date of birth is also only sample input.

## 4. Example Login

```text
LOGIN
--------------------------------------------
Enter Account Number: 123456789012
Enter PIN: ****

Welcome, Sanika Kadam!
```

The program permits up to three login attempts. Failed attempts display a message and the number of attempts remaining.

## 5. Account Menu

After successful login, the application displays:

```text
============================================
ACCOUNT MENU | Sanika Kadam | Savings
============================================
1. Display Customer Details
2. Money Transaction
3. Cards (Debit / Credit)
4. Services & Maintenance
5. Loans
6. Locker
7. Logout
Enter Your Choice:
```

## 6. Money Transaction Features

The Money Transaction menu provides:

```text
MONEY TRANSACTION
--------------------------------------------
1. Check Balance
2. Deposit
3. Withdraw
4. Transfer
5. Mini Statement
6. Back
```

Examples of supported actions:

- **Check balance:** Displays the current balance and required minimum balance.
- **Deposit:** Adds the entered amount to the account balance.
- **Withdraw:** Deducts money if the minimum balance requirement is maintained.
- **Transfer:** Moves money to another account created in the same running session.
- **Mini statement:** Displays recent transaction dates, types, amounts, balances, and notes.

## 7. Card Services

The card menu supports:

1. Apply for a debit card
2. Apply for a credit card
3. View cards
4. Make a debit-card purchase
5. Make a credit-card purchase
6. Pay a credit-card bill
7. Block or unblock a card

Credit-card application requires a minimum account balance of ₹10,000 in this demo. The program simulates card operations; it does not connect to a real payment network.

## 8. Services and Maintenance

The customer can:

- Change the account PIN
- Update the mobile number
- Pay the account maintenance charge
- Request a cheque book

Configured maintenance charges are ₹50 per quarter for Savings accounts and ₹200 per quarter for Current accounts. The current code lets the user initiate payment manually; it does not automatically charge the account every quarter.

## 9. Loan Section

Available demo loan types:

| Loan type | Annual interest rate | Maximum tenure |
|---|---:|---:|
| Home Loan | 8.5% | 30 years |
| Education Loan | 9.5% | 15 years |
| Car Loan | 9.0% | 7 years |
| Agricultural Loan | 7.0% | 10 years |

The program estimates monthly EMI using the principal, monthly interest rate, and repayment period. It rejects an application when the calculated EMI exceeds half of the entered monthly income. This is a simplified project rule, not a real loan-approval process.

## 10. Locker Section

The locker menu supports:

- Creating a Small, Medium, or Large locker
- Accessing a locker with its PIN
- Viewing locker details
- Closing a locker

| Locker size | Annual rent |
|---|---:|
| Small | ₹1,500 |
| Medium | ₹3,000 |
| Large | ₹6,000 |

The rent is deducted when the locker is created. In the current code, closing a locker does not refund the rent.

## 11. Input Validation and Security Features

- Validates numeric menu choices and transaction amounts.
- Validates date of birth format and calculates age.
- Requires a 10-digit mobile number.
- Requires a four-digit PIN.
- Hashes stored account and locker PINs with SHA-256.
- Limits login to three attempts.
- Prevents withdrawals and transfers that would take the balance below the configured minimum.

These are introductory safeguards. The program is not suitable for real customer or financial data.

## 12. How to Run

1. Save the Python program as `bank_system.py`.
2. Open a terminal in the folder containing the file.
3. Run:

   ```bash
   python bank_system.py
   ```

4. Choose **Create Account**.
5. Record the generated account number.
6. Log in and explore the available services.
7. Choose **Exit** to close the application.

## 13. Conclusion

The Bank Management System demonstrates how Python can be used to build a modular, menu-driven application. It brings together account management, transaction processing, card services, loan EMI calculations, and locker management in one console program.

The project provides practical experience with functions, dictionaries, lists, validation, hashing, date/time operations, and conditional logic. Future versions could use a database for persistent storage and add stronger security, testing, and a graphical user interface.

---

**Prepared by: Sanika Kadam**
