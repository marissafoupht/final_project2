from PyQt6.QtWidgets import *
from bank_account_gui import *
import csv
import re
class Logic(QMainWindow, Ui_bank_account_mainwindow):
    """
    Controller class for project. Code to make application work is placed here.
    imports PyQt5 widgets and bank_account_gui
    """
    def __init__(self):
        """
        Method Initializes logic class and sets up Ui.

        sets current widget to home_page

        calls login function when login button clicked
        calls logout function when logout button clicked

        creates private variables username, password, and balance

        :param: = None
        :return: None
        """
        super().__init__()
        self.setupUi(self)

        self.stackedWidget.setCurrentWidget(self.home_page)

        self.button_login.clicked.connect(lambda: self.login())
        self.button_logout.clicked.connect(lambda: self.logout())

        self.__username = ""
        self.__password = ""
        self.__balance = 0

    def login(self) -> None:
        """
        username = user input text
        password = user input text

        Method checks if user has input text in both username and password boxes
        If both found, calls login_verification function
        If only username found, asks for password
        If only password found, asks for username
        If both empty, asks for username and password

        :param: = none
        :return: = none
        """
        username = self.input_username.text()
        password = self.input_password.text()
        if username and password:
            self.login_verification()
        elif username:
            self.label_welcome.setText(f'Password required.')
        elif password:
            self.label_welcome.setText(f'Username required.')
        else:
            self.label_welcome.setText(f'Password and Username required.')

    def login_verification(self) -> None:
        """
        Opens logins_usernames csv file and read contents, then adds them to user_dict

        username = username input text
        password = password input text

        Method checks if username and password are in user_dict:
            If found:
                sets username, password, and balance to private variables.
                sends welcome user message
                shows user account balance
                sets current stacked widget to choose_option_page
                connects deposit or withdrawal button to related function
            if not fount:
                sends wrong username or password message

        :param: = none
        :return: = none
        """
        with open('logins_usernames.csv', 'r') as file:
            reader = csv.reader(file)
            user_dict = {rows[0]:[rows[1], rows[2]] for rows in reader}

        username = self.input_username.text()
        password = self.input_password.text()
        if username in user_dict:
            if password in user_dict[username]:
                self.__username = username
                self.__password = password
                self.__balance = float(user_dict[username][1])
                self.label_welcome.setText(f'Welcome {username}')
                self.label_account_balance.setText(f'Account Balance: ${self.__balance}')
                self.stackedWidget.setCurrentWidget(self.choose_option_page)
                self.button_deposit.clicked.connect(lambda: self.deposit())
                self.button_withdrawal.clicked.connect(lambda: self.withdrawal())
        else:
            self.label_welcome.setText(f'Username or password is incorrect.')

    def deposit(self) -> None:
        """
        Method sets current stacked widget to deposit_page
        connects deposit submit button with deposit_submit() func.

        :param: = none
        :return: = none
        """
        self.stackedWidget.setCurrentWidget(self.deposit_page)
        self.button_deposit_submit.clicked.connect(lambda: self.deposit_submit())

    def deposit_submit(self) -> None:
        """
        Takes deposit amount input by user and first matches it to the pattern provided:
        (starts with digit(s), must have decimal, two digits after decimal)
        If pattern match fails, denied message printed.

        If pattern match succeeds, deposit amount turned into float().
            If deposit amount greater 1000000000000, denied message printed.
            If deposit amount less than or equal to 0, denied message printed.

            If all comparisons succeed:
            deposit amount is added to user balance
            new account balance is printed
            current stacked widget is set back to choose_option_page

        :param: = none
        :return: = none
        """
        depo_amount = self.input_deposit_amount.text()
        if re.match(r'^\d+\.\d{2}$', depo_amount):
            depo_amount = float(depo_amount)
            if depo_amount > 1000000000000.00:
                self.label_deposit_exceptions.setText(f'Deposit denied. Amount exceeds limit.')
            else:
                if depo_amount <= 0:
                    self.label_deposit_exceptions.setText(f'Deposit denied. Amount too small.')
                else:
                    self.__balance = round(depo_amount + self.__balance, 2)
                    self.label_account_balance.setText(f'Account Balance: ${self.__balance}')
                    self.stackedWidget.setCurrentWidget(self.choose_option_page)
        else:
            self.label_deposit_exceptions.setText(f'Deposit denied. Enter valid number with two decimals.')


    def withdrawal(self) -> None:
        """
        Method sets current stacked widget to withdrawal_page
        Connects withdrawal submit button with withdrawal_submit() func.

        :param: = none
        :return: = none
        """
        self.stackedWidget.setCurrentWidget(self.withdrawal_page)
        self.button_withdrawal_submit.clicked.connect(lambda: self.withdrawal_submit())

    def withdrawal_submit(self) -> None:
        """
        Takes withdrawal amount input by user and first matches it to the pattern provided:
        (starts with digit(s), must have decimal, two digits after decimal)
        If pattern match fails, denied message printed.

        If pattern match succeeds, withdrawal amount turned into float().
            If withdrawal amount greater than user balance, denied message printed.
            If withdrawal amount less than or equal to 0, denied message printed.

            If all comparisons succeed:
            withdrawal amount is deducted from user balance
            new account balance is printed
            current stacked widget is set back to choose_option_page

        :param: = none
        :return: = none
        """
        with_amount = self.input_withdrawal_amount.text()
        if re.match(r'^\d+\.\d{2}$', with_amount):
            with_amount = float(with_amount)
            if with_amount > self.__balance:
                self.label_withdrawal_exceptions.setText(f'Withdrawal denied. Amount exceeds balance')
            else:
                if with_amount <= 0:
                    self.label_withdrawal_exceptions.setText(f'Withdrawal denied. Amount too small. ')
                else:
                    self.__balance = round(self.__balance - with_amount, 2)
                    self.label_account_balance.setText(f'Account Balance: ${self.__balance}')
                    self.stackedWidget.setCurrentWidget(self.choose_option_page)
        else:
            self.label_withdrawal_exceptions.setText(f'Withdrawal denied. Enter valid number with two decimals.')

    def logout(self) -> none:
        """
        Method opens logins_username csv and reads contents, adding them to dict.
        Method then reopens csv file and writes new balance of user.

        When done writing, all application labels and inputs are cleared,
        and current stacked widget is set back to home_page.

        :param: = none
        :return: = none
        """
        dict = []
        with open('logins_usernames.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == self.__username:
                    row[2] = str(self.__balance)
                dict.append(row)
        with open('logins_usernames.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(dict)
        self.label_welcome.setText(f'')
        self.label_account_balance.setText(f'')
        self.input_username.clear()
        self.input_password.clear()
        self.stackedWidget.setCurrentWidget(self.home_page)