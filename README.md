<div align="center">

# 🏦 Bank Management System

### A menu-driven banking application built with Python

Manage customer accounts, transactions, cards, loans, and locker services through a simple console interface.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Application](https://img.shields.io/badge/Type-Console%20Application-2E8B57?style=for-the-badge)
![Status](https://img.shields.io/badge/Project-Educational-orange?style=for-the-badge)

</div>

---

## 📌 About the Project

The **Bank Management System** is a Python-based console application that simulates common banking operations. It allows a customer to create an account, log in using a PIN, manage money, apply for cards and loans, request a cheque book, and use locker services.

The project demonstrates core Python concepts such as functions, dictionaries, loops, conditional statements, input validation, exception handling, date/time handling, random number generation, and hashing.

> **Project type:** Educational/demo project. It is not connected to a real bank and should not be used to store real financial or personal information.

## ✨ Features

| Feature | Description |
|---|---|
| 👤 Account creation | Creates a Savings or Current account after validating customer details and minimum balance. |
| 🔐 Login security | Checks a four-digit PIN and allows up to three login attempts. |
| 💰 Transactions | Supports deposits, withdrawals, transfers, balance checks, and mini statements. |
| 💳 Card services | Simulates debit/credit card applications, purchases, bill payments, and card blocking. |
| 🧾 Account services | Supports PIN changes, mobile number updates, maintenance charges, and cheque-book requests. |
| 🏠 Loan management | Simulates loan applications, EMI calculation, loan details, and EMI payments. |
| 🔒 Locker services | Supports locker creation, access, viewing details, and closing a locker. |
| 📋 Transaction history | Records transactions with timestamps, amounts, balances, and notes. |
| ✅ Input validation | Validates numeric inputs, dates, mobile numbers, and four-digit PINs. |

## 🧰 Technologies Used

- **Python** — application logic
- `random` — generates demo account, card, and locker numbers
- `hashlib` — hashes PINs using SHA-256
- `datetime` — validates dates and records transaction timestamps
- **Dictionaries and lists** — store account data and transaction history during execution

No third-party Python packages are required.

## 🚀 Getting Started

### Requirements

- Python 3.10 or later recommended
- Terminal, Command Prompt, PowerShell, or VS Code

### 1. Download or clone the project

If the project is on GitHub:

```bash
git clone <your-repository-url>
cd <your-project-folder>
```

Alternatively, save the Python source code in a file named `bank_system.py`.

### 2. Run the application

```bash
python bank_system.py
```

On some Windows installations, use:

```bash
py bank_system.py
```

### 3. Use the main menu

```text
------ BANK SYSTEM ------
1. Create Account
2. Login
3. Exit
```

Create an account first, note the generated account number, and then log in with the PIN you created.

## 🧭 Application Menu

After logging in, the customer can access:

1. Display Customer Details
2. Money Transaction
3. Cards (Debit / Credit)
4. Services & Maintenance
5. Loans
6. Locker
7. Logout

## 💵 Rules and Demo Values

| Item | Demo rule |
|---|---|
| Minimum Savings balance | ₹1,000 |
| Minimum Current balance | ₹5,000 |
| Quarterly maintenance charge | Savings: ₹50; Current: ₹200 |
| Cheque-book fee | ₹100 |
| Credit-card eligibility balance | ₹10,000 |
| Login attempts | 3 |
| Customer age | 18 years or older |
| Mobile number | 10 digits |
| PIN | 4 digits |
| Locker rent per year | Small: ₹1,500; Medium: ₹3,000; Large: ₹6,000 |

Loan rates and maximum tenures are configured in the source code. These are illustrative values for this project, not live bank offers.

## 📁 Suggested Project Structure

```text
Bank-Management-System/
├── bank_system.py
├── README.md
└── output.md
```

## 🧠 Concepts Demonstrated

- Functions and modular programming
- Dictionaries and lists
- `if` / `elif` / `else` conditions
- `while` and `for` loops
- Input validation and `try` / `except`
- Date parsing with `datetime`
- PIN hashing with `hashlib`
- EMI calculation using the reducing-balance formula
- Transaction records and menu-driven program flow

## ⚠️ Important Limitations

This implementation is a learning prototype, not production banking software.

- Account data is stored in an in-memory dictionary and is lost when the program exits.
- SHA-256 alone is not a recommended production method for storing PINs; use a dedicated password/PIN hashing approach with salts and appropriate controls.
- Randomly generated account/card/locker numbers are for demonstration and do not implement real banking standards, checksums, or guaranteed uniqueness across all systems.
- The application prints full card numbers and CVVs when issuing cards. Never display or store sensitive card data this way in a real system.
- Card purchases, loan approvals, and transfers are simulated; there is no bank, payment gateway, credit bureau, or external verification.
- The maintenance fee can be paid repeatedly whenever selected; automatic quarterly scheduling is not implemented.
- Use only fictional test data.

## 🔮 Possible Future Improvements

- Store accounts in MySQL or SQLite so data persists between runs.
- Add automated tests for deposits, withdrawals, transfers, and EMI calculations.
- Add stronger authentication, salted PIN hashing, and secure session handling.
- Add transaction limits, duplicate-number protection, and audit logging.
- Add a graphical interface or web dashboard.
- Implement dates and rules for scheduled maintenance charges and loan repayment.

## 👩‍💻 Author

**Sanika Kadam**

*Python Banking System — Educational Project*

---

<div align="center">

Made with 🐍 Python

</div>
