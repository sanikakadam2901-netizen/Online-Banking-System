import random
import hashlib
from datetime import datetime

# ---------------------------------------------------------------- CONSTANTS
MIN_BALANCE = {'Savings': 1000, 'Current': 5000}
MAINTENANCE_CHARGE = {'Savings': 50, 'Current': 200}      # per quarter
CHEQUE_BOOK_FEE = 100
CREDIT_CARD_MIN_BALANCE = 10000
MAX_LOGIN_ATTEMPTS = 3
LOCKER_RENT = {'Small': 1500, 'Medium': 3000, 'Large': 6000}   # per year

LOANS = {
    # name: (annual interest %, max years)
    'Home Loan': (8.5, 30),
    'Education Loan': (9.5, 15),
    'Car Loan': (9.0, 7),
    'Agricultural Loan': (7.0, 10),
}

# ---------------------------------------------------------------- DATA STORE
accounts = {}          # {account_number: account_dict}


# ---------------------------------------------------------------- HELPERS
def line(char='-', n=44):
    print(char * n)


def hash_pin(pin):
    return hashlib.sha256(pin.encode()).hexdigest()


def get_int(prompt, min_value=None, max_value=None):
    """Keep asking until the user enters a valid integer."""
    while True:
        try:
            value = int(input(prompt).strip())
        except ValueError:
            print('Please enter a valid number.')
            continue
        if min_value is not None and value < min_value:
            print(f'Value must be at least {min_value}.')
            continue
        if max_value is not None and value > max_value:
            print(f'Value must be at most {max_value}.')
            continue
        return value


def get_text(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print('This field cannot be empty.')


def get_pin(prompt='Enter 4-digit PIN: '):
    while True:
        pin = input(prompt).strip()
        if pin.isdigit() and len(pin) == 4:
            return pin
        print('PIN must be exactly 4 digits.')


def get_dob():
    while True:
        text = input('Enter Date of Birth (DD/MM/YYYY): ').strip()
        try:
            dob = datetime.strptime(text, '%d/%m/%Y')
        except ValueError:
            print('Invalid format. Example: 25/12/1998')
            continue
        today = datetime.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return text, age


def get_mobile():
    while True:
        mobile = input('Enter Mobile Number (10 digits): ').strip()
        if mobile.isdigit() and len(mobile) == 10:
            return mobile
        print('Mobile number must be 10 digits.')


def new_account_number():
    while True:
        number = random.randint(100000000000, 999999999999)
        if number not in accounts:
            return number


def add_txn(acc, kind, amount, note=''):
    acc['transactions'].append({
        'time': datetime.now().strftime('%d-%m-%Y %H:%M'),
        'type': kind,
        'amount': amount,
        'balance': acc['balance'],
        'note': note,
    })


def can_debit(acc, amount):
    """A debit is allowed only if the minimum balance stays maintained."""
    minimum = MIN_BALANCE[acc['type']]
    if amount <= 0:
        print('Amount must be greater than 0.')
        return False
    if acc['balance'] - amount < minimum:
        print(f"Transaction denied. Minimum balance of Rs.{minimum} "
              f"must be maintained ({acc['type']} account).")
        return False
    return True


def generate_card_number(prefix):
    return prefix + ''.join(str(random.randint(0, 9)) for _ in range(15))


def mask(number):
    return '**** **** **** ' + number[-4:]


def expiry_date():
    today = datetime.today()
    return f'{today.month:02d}/{today.year + 5}'


# ---------------------------------------------------------------- CREATE ACCOUNT
def create_account():
    line('=')
    print('ACCOUNT CREATION')
    line('=')
    name = get_text('Enter Your Name: ')
    gender = get_text('Enter Your Gender: ')
    dob, age = get_dob()
    if age < 18:
        print('You are under age to open an account (18+ required).')
        return
    mobile = get_mobile()

    print('\nChoose Account Type:')
    print(f"1. Current Account (min balance Rs.{MIN_BALANCE['Current']})")
    print(f"2. Savings Account (min balance Rs.{MIN_BALANCE['Savings']})")
    choice = get_int('Enter Your Choice: ', 1, 2)
    acc_type = 'Current' if choice == 1 else 'Savings'
    minimum = MIN_BALANCE[acc_type]

    balance = get_int('Enter Initial Balance: ', 0)
    if balance < minimum:
        print(f'Minimum balance for a {acc_type} account is Rs.{minimum}!')
        return

    pin = get_pin('Set a 4-digit PIN: ')
    acc_no = new_account_number()

    accounts[acc_no] = {
        'acc_no': acc_no,
        'name': name,
        'gender': gender,
        'age': age,
        'dob': dob,
        'mobile': mobile,
        'type': acc_type,
        'balance': balance,
        'pin_hash': hash_pin(pin),
        'transactions': [],
        'debit_card': None,
        'credit_card': None,
        'loans': {},
        'cheque_book': False,
        'locker': None,
    }
    add_txn(accounts[acc_no], 'OPENING', balance, 'Account opened')

    line('=')
    print('ACCOUNT CREATED SUCCESSFULLY')
    print(f'Account Holder : {name}')
    print(f'Account Type   : {acc_type}')
    print(f'Balance        : Rs.{balance}')
    print(f'Account Number : {acc_no}   <-- note this down')
    line('=')


# ---------------------------------------------------------------- LOGIN
def login():
    print('\nLOGIN')
    line()
    acc_no = get_int('Enter Account Number: ')
    acc = accounts.get(acc_no)
    for attempt in range(1, MAX_LOGIN_ATTEMPTS + 1):
        pin = input('Enter PIN: ').strip()
        if acc and acc['pin_hash'] == hash_pin(pin):
            print(f"\nWelcome, {acc['name']}!")
            return acc
        left = MAX_LOGIN_ATTEMPTS - attempt
        print(f'Invalid account number or PIN. Attempts left: {left}')
    print('Too many failed attempts. Returning to main menu.')
    return None


# ---------------------------------------------------------------- ACCOUNT FUNCTIONS
def display_details(acc):
    line('=')
    print('CUSTOMER DETAILS')
    line('=')
    rows = [
        ('Account Number:', acc['acc_no']),
        ('Account Holder:', acc['name']),
        ('Gender:', acc['gender']),
        ('Age:', acc['age']),
        ('Date of Birth:', acc['dob']),
        ('Mobile Number:', acc['mobile']),
        ('Account Type:', acc['type']),
        ('Current Balance:', f"Rs.{acc['balance']}"),
        ('Debit Card:', 'Yes' if acc['debit_card'] else 'No'),
        ('Credit Card:', 'Yes' if acc['credit_card'] else 'No'),
        ('Active Loans:', ', '.join(acc['loans']) or 'None'),
        ('Locker:', acc['locker']['number'] if acc['locker'] else 'None'),
    ]
    for label, value in rows:
        print(f'{label:<18} {value}')
    line('=')


def check_balance(acc):
    print(f"Available Balance: Rs.{acc['balance']}  "
          f"(minimum required: Rs.{MIN_BALANCE[acc['type']]})")


def deposit(acc):
    amount = get_int('Enter amount to deposit: ', 1)
    acc['balance'] += amount
    add_txn(acc, 'CREDIT', amount, 'Cash deposit')
    print(f"Deposited Rs.{amount}. New balance: Rs.{acc['balance']}")


def withdraw(acc):
    amount = get_int('Enter amount to withdraw: ', 1)
    if can_debit(acc, amount):
        acc['balance'] -= amount
        add_txn(acc, 'DEBIT', amount, 'Cash withdrawal')
        print(f"Withdrawn Rs.{amount}. New balance: Rs.{acc['balance']}")


def transfer(acc):
    target_no = get_int('Enter receiver account number: ')
    target = accounts.get(target_no)
    if target is None:
        print('Receiver account not found.')
        return
    if target_no == acc['acc_no']:
        print('You cannot transfer to your own account.')
        return
    amount = get_int('Enter amount to transfer: ', 1)
    if not can_debit(acc, amount):
        return
    acc['balance'] -= amount
    target['balance'] += amount
    add_txn(acc, 'DEBIT', amount, f'Transfer to {target_no}')
    add_txn(target, 'CREDIT', amount, f"Transfer from {acc['acc_no']}")
    print(f"Transferred Rs.{amount} to {target['name']}. New balance: Rs.{acc['balance']}")


def mini_statement(acc, count=10):
    line('=')
    print(f'MINI STATEMENT (last {count} transactions)')
    line('=')
    print(f"{'Date':<17}{'Type':<9}{'Amount':>9}{'Balance':>10}  Note")
    for t in acc['transactions'][-count:]:
        print(f"{t['time']:<17}{t['type']:<9}{t['amount']:>9}{t['balance']:>10}  {t['note']}")
    line('=')


def money_transaction_menu(acc):
    while True:
        line()
        print('MONEY TRANSACTION')
        print('1. Check Balance\n2. Deposit\n3. Withdraw\n4. Transfer\n5. Mini Statement\n6. Back')
        choice = get_int('Enter Your Choice: ', 1, 6)
        if choice == 1:
            check_balance(acc)
        elif choice == 2:
            deposit(acc)
        elif choice == 3:
            withdraw(acc)
        elif choice == 4:
            transfer(acc)
        elif choice == 5:
            mini_statement(acc)
        else:
            return


# ---------------------------------------------------------------- CARDS
def apply_debit_card(acc):
    if acc['debit_card']:
        print('You already have a debit card.')
        return
    acc['debit_card'] = {
        'number': generate_card_number('4'),
        'cvv': f'{random.randint(0, 999):03d}',
        'expiry': expiry_date(),
        'blocked': False,
        'daily_limit': 50000,
    }
    card = acc['debit_card']
    print('Debit card issued successfully!')
    print(f"Card Number : {card['number']}")
    print(f"Expiry      : {card['expiry']}    CVV: {card['cvv']}")
    print(f"Daily limit : Rs.{card['daily_limit']}")


def apply_credit_card(acc):
    if acc['credit_card']:
        print('You already have a credit card.')
        return
    if acc['balance'] < CREDIT_CARD_MIN_BALANCE:
        print(f'Credit card needs a balance of at least Rs.{CREDIT_CARD_MIN_BALANCE}.')
        return
    limit = min(acc['balance'] * 3, 200000)
    acc['credit_card'] = {
        'number': generate_card_number('5'),
        'cvv': f'{random.randint(0, 999):03d}',
        'expiry': expiry_date(),
        'blocked': False,
        'limit': limit,
        'used': 0,
    }
    card = acc['credit_card']
    print('Credit card issued successfully!')
    print(f"Card Number  : {card['number']}")
    print(f"Expiry       : {card['expiry']}    CVV: {card['cvv']}")
    print(f"Credit limit : Rs.{limit}")


def debit_card_purchase(acc):
    card = acc['debit_card']
    if not card:
        print('You do not have a debit card.')
        return
    if card['blocked']:
        print('Your debit card is blocked.')
        return
    amount = get_int('Enter purchase amount: ', 1)
    if amount > card['daily_limit']:
        print(f"Exceeds daily limit of Rs.{card['daily_limit']}.")
        return
    if can_debit(acc, amount):
        acc['balance'] -= amount
        add_txn(acc, 'DEBIT', amount, f"Debit card {card['number'][-4:]}")
        print(f"Payment successful. New balance: Rs.{acc['balance']}")


def credit_card_purchase(acc):
    card = acc['credit_card']
    if not card:
        print('You do not have a credit card.')
        return
    if card['blocked']:
        print('Your credit card is blocked.')
        return
    amount = get_int('Enter purchase amount: ', 1)
    available = card['limit'] - card['used']
    if amount > available:
        print(f'Insufficient credit. Available: Rs.{available}')
        return
    card['used'] += amount
    print(f"Payment successful. Credit used: Rs.{card['used']} / Rs.{card['limit']}")


def pay_credit_card_bill(acc):
    card = acc['credit_card']
    if not card:
        print('You do not have a credit card.')
        return
    if card['used'] == 0:
        print('No outstanding credit card bill.')
        return
    print(f"Outstanding bill: Rs.{card['used']}")
    amount = get_int('Enter amount to pay: ', 1, card['used'])
    if can_debit(acc, amount):
        acc['balance'] -= amount
        card['used'] -= amount
        add_txn(acc, 'DEBIT', amount, 'Credit card bill payment')
        print(f"Bill paid. Outstanding: Rs.{card['used']}. Balance: Rs.{acc['balance']}")


def toggle_block(acc):
    print('1. Debit Card\n2. Credit Card')
    which = get_int('Select card: ', 1, 2)
    card = acc['debit_card'] if which == 1 else acc['credit_card']
    if not card:
        print('You do not have that card.')
        return
    card['blocked'] = not card['blocked']
    print('Card BLOCKED.' if card['blocked'] else 'Card UNBLOCKED.')


def view_cards(acc):
    line('=')
    print('YOUR CARDS')
    line('=')
    d, c = acc['debit_card'], acc['credit_card']
    if d:
        print(f"Debit  : {mask(d['number'])}  Exp {d['expiry']}  "
              f"{'BLOCKED' if d['blocked'] else 'ACTIVE'}  Daily limit Rs.{d['daily_limit']}")
    else:
        print('Debit  : not issued')
    if c:
        print(f"Credit : {mask(c['number'])}  Exp {c['expiry']}  "
              f"{'BLOCKED' if c['blocked'] else 'ACTIVE'}  Used Rs.{c['used']} / Rs.{c['limit']}")
    else:
        print('Credit : not issued')
    line('=')


def cards_menu(acc):
    while True:
        line()
        print('CARD SERVICES')
        print('1. Apply Debit Card\n2. Apply Credit Card\n3. View Cards\n'
              '4. Debit Card Purchase\n5. Credit Card Purchase\n6. Pay Credit Card Bill\n'
              '7. Block / Unblock Card\n8. Back')
        choice = get_int('Enter Your Choice: ', 1, 8)
        if choice == 1:
            apply_debit_card(acc)
        elif choice == 2:
            apply_credit_card(acc)
        elif choice == 3:
            view_cards(acc)
        elif choice == 4:
            debit_card_purchase(acc)
        elif choice == 5:
            credit_card_purchase(acc)
        elif choice == 6:
            pay_credit_card_bill(acc)
        elif choice == 7:
            toggle_block(acc)
        else:
            return


# ---------------------------------------------------------------- SERVICES / MAINTENANCE
def change_pin(acc):
    old = input('Enter current PIN: ').strip()
    if hash_pin(old) != acc['pin_hash']:
        print('Incorrect PIN.')
        return
    new = get_pin('Enter new 4-digit PIN: ')
    acc['pin_hash'] = hash_pin(new)
    print('PIN changed successfully.')


def update_mobile(acc):
    acc['mobile'] = get_mobile()
    print('Mobile number updated.')


def pay_maintenance(acc):
    fee = MAINTENANCE_CHARGE[acc['type']]
    print(f"{acc['type']} account maintenance charge: Rs.{fee} per quarter.")
    if input('Pay now? (y/n): ').strip().lower() != 'y':
        return
    if can_debit(acc, fee):
        acc['balance'] -= fee
        add_txn(acc, 'DEBIT', fee, 'Account maintenance charge')
        print(f"Paid Rs.{fee}. Balance: Rs.{acc['balance']}")


def request_cheque_book(acc):
    if acc['cheque_book']:
        print('A cheque book has already been issued to you.')
        return
    print(f'Cheque book fee: Rs.{CHEQUE_BOOK_FEE}')
    if can_debit(acc, CHEQUE_BOOK_FEE):
        acc['balance'] -= CHEQUE_BOOK_FEE
        acc['cheque_book'] = True
        add_txn(acc, 'DEBIT', CHEQUE_BOOK_FEE, 'Cheque book fee')
        print('Cheque book requested. It will be delivered in 5-7 working days.')


def services_menu(acc):
    while True:
        line()
        print('SERVICES & MAINTENANCE')
        print('1. Change PIN\n2. Update Mobile Number\n3. Pay Maintenance Charges\n'
              '4. Request Cheque Book\n5. Back')
        choice = get_int('Enter Your Choice: ', 1, 5)
        if choice == 1:
            change_pin(acc)
        elif choice == 2:
            update_mobile(acc)
        elif choice == 3:
            pay_maintenance(acc)
        elif choice == 4:
            request_cheque_book(acc)
        else:
            return


# ---------------------------------------------------------------- LOANS
def calculate_emi(principal, annual_rate, years):
    r = annual_rate / 12 / 100
    n = years * 12
    return principal * r * (1 + r) ** n / ((1 + r) ** n - 1)


def apply_loan(acc):
    names = list(LOANS)
    line('=')
    print('LOAN SECTION')
    line('=')
    for i, name in enumerate(names, 1):
        rate, max_years = LOANS[name]
        print(f'{i}. {name:<18} {rate}% p.a.  (max {max_years} years)')
    print(f'{len(names) + 1}. Back')
    choice = get_int('Enter Your Choice: ', 1, len(names) + 1)
    if choice == len(names) + 1:
        return

    loan_name = names[choice - 1]
    rate, max_years = LOANS[loan_name]
    if loan_name in acc['loans']:
        print(f'You already have an active {loan_name}.')
        return

    print(f'\n--- {loan_name.upper()} ---')
    amount = get_int('Enter Loan Amount: ', 1000)
    income = get_int('Enter Annual Income: ', 1)
    years = get_int(f'In how many years will you clear the loan (1-{max_years})? ', 1, max_years)

    emi = calculate_emi(amount, rate, years)
    monthly_income = income / 12
    if emi > monthly_income / 2:
        print(f'Not eligible: EMI Rs.{emi:.2f} exceeds 50% of monthly income '
              f'(Rs.{monthly_income / 2:.2f}).')
        return

    months = years * 12
    acc['loans'][loan_name] = {
        'principal': amount,
        'rate': rate,
        'years': years,
        'emi': round(emi, 2),
        'months_left': months,
    }
    acc['balance'] += amount
    add_txn(acc, 'CREDIT', amount, f'{loan_name} disbursed')

    line('=')
    print('You are eligible. LOAN SUCCESSFUL')
    print(f"Loan Holder  : {acc['name']}")
    print(f'Loan Type    : {loan_name}')
    print(f'Loan Amount  : Rs.{amount}')
    print(f'Interest     : {rate}% p.a.')
    print(f'Tenure       : {years} years ({months} months)')
    print(f'Monthly EMI  : Rs.{emi:.2f}')
    print(f'Total payable: Rs.{emi * months:.2f}')
    print(f"Loan amount credited. New balance: Rs.{acc['balance']}")
    line('=')


def view_loans(acc):
    if not acc['loans']:
        print('You have no active loans.')
        return
    line('=')
    print('YOUR LOANS')
    line('=')
    for name, loan in acc['loans'].items():
        outstanding = loan['emi'] * loan['months_left']
        print(f"{name}: Rs.{loan['principal']} @ {loan['rate']}% | EMI Rs.{loan['emi']} | "
              f"{loan['months_left']} months left | Outstanding ~Rs.{outstanding:.2f}")
    line('=')


def pay_emi(acc):
    if not acc['loans']:
        print('You have no active loans.')
        return
    names = list(acc['loans'])
    for i, name in enumerate(names, 1):
        print(f"{i}. {name} (EMI Rs.{acc['loans'][name]['emi']})")
    choice = get_int('Select loan to pay EMI for: ', 1, len(names))
    name = names[choice - 1]
    loan = acc['loans'][name]
    emi = int(-(-loan['emi'] // 1))        # round up to a whole rupee
    if can_debit(acc, emi):
        acc['balance'] -= emi
        loan['months_left'] -= 1
        add_txn(acc, 'DEBIT', emi, f'{name} EMI')
        print(f"EMI of Rs.{emi} paid. Months left: {loan['months_left']}")
        if loan['months_left'] <= 0:
            del acc['loans'][name]
            print(f'Congratulations! Your {name} is fully repaid.')


def loan_menu(acc):
    while True:
        line()
        print('LOANS')
        print('1. Apply for Loan\n2. View My Loans\n3. Pay EMI\n4. Back')
        choice = get_int('Enter Your Choice: ', 1, 4)
        if choice == 1:
            apply_loan(acc)
        elif choice == 2:
            view_loans(acc)
        elif choice == 3:
            pay_emi(acc)
        else:
            return


# ---------------------------------------------------------------- LOCKER
def create_locker(acc):
    if acc['locker']:
        print('A locker already exists for this account.')
        return
    sizes = list(LOCKER_RENT)
    for i, size in enumerate(sizes, 1):
        print(f'{i}. {size:<7} Rs.{LOCKER_RENT[size]} per year')
    size = sizes[get_int('Select locker size: ', 1, len(sizes)) - 1]
    rent = LOCKER_RENT[size]
    if not can_debit(acc, rent):
        return
    pin = get_pin('Create a 4-digit locker PIN: ')
    number = random.randint(10000, 99999)
    acc['balance'] -= rent
    add_txn(acc, 'DEBIT', rent, f'{size} locker rent')
    acc['locker'] = {'number': number, 'size': size, 'pin_hash': hash_pin(pin), 'status': 'Active'}
    print('\nLocker created successfully!')
    print(f'Locker Number: {number}   Size: {size}   Rent paid: Rs.{rent}')
    print('Keep your PIN secret.')


def access_locker(acc):
    locker = acc['locker']
    if not locker:
        print('No locker found. Please create a locker first.')
        return
    pin = input('Enter your locker PIN: ').strip()
    if hash_pin(pin) == locker['pin_hash']:
        print('\nLocker access successful.')
        print(f"Locker Number: {locker['number']}")
        print(f"Locker Status: {locker['status']}")
    else:
        print('Incorrect PIN.')


def view_locker(acc):
    locker = acc['locker']
    if not locker:
        print('No locker found for this account.')
        return
    line('=')
    print('LOCKER DETAILS')
    line('=')
    print(f"Account Holder: {acc['name']}")
    print(f"Locker Number : {locker['number']}")
    print(f"Size          : {locker['size']}")
    print(f"Status        : {locker['status']}")
    line('=')


def close_locker(acc):
    if not acc['locker']:
        print('No locker found for this account.')
        return
    pin = input('Enter your locker PIN to confirm: ').strip()
    if hash_pin(pin) != acc['locker']['pin_hash']:
        print('Incorrect PIN.')
        return
    acc['locker'] = None
    print('Locker closed. Rent is non-refundable.')


def locker_menu(acc):
    while True:
        line()
        print('LOCKER SECTION')
        print('1. Create Locker\n2. Access Locker\n3. View Locker Details\n4. Close Locker\n5. Back')
        choice = get_int('Enter Your Choice: ', 1, 5)
        if choice == 1:
            create_locker(acc)
        elif choice == 2:
            access_locker(acc)
        elif choice == 3:
            view_locker(acc)
        elif choice == 4:
            close_locker(acc)
        else:
            return


# ---------------------------------------------------------------- MENUS
def user_menu(acc):
    while True:
        line('=')
        print(f"ACCOUNT MENU  |  {acc['name']}  |  {acc['type']}")
        line('=')
        print('1. Display Customer Details\n2. Money Transaction\n3. Cards (Debit / Credit)\n'
              '4. Services & Maintenance\n5. Loans\n6. Locker\n7. Logout')
        choice = get_int('Enter Your Choice: ', 1, 7)
        if choice == 1:
            display_details(acc)
        elif choice == 2:
            money_transaction_menu(acc)
        elif choice == 3:
            cards_menu(acc)
        elif choice == 4:
            services_menu(acc)
        elif choice == 5:
            loan_menu(acc)
        elif choice == 6:
            locker_menu(acc)
        else:
            print('Logged out successfully.')
            return


def welcome():
    while True:
        line('=')
        print('------ BANK SYSTEM ------')
        line('=')
        print('1. Create Account\n2. Login\n3. Exit')
        choice = get_int('Enter Your Choice: ', 1, 3)
        if choice == 1:
            create_account()
        elif choice == 2:
            if not accounts:
                print('No accounts exist yet. Please create an account first.')
                continue
            acc = login()
            if acc:
                user_menu(acc)
        else:
            print('Thank You....')
            break


if __name__ == '__main__':
    welcome()
