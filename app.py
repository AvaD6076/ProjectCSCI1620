from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

# Simulated database of users
users = {}

class User:
    def __init__(self, first_name, last_name, pin, balance=0):
        self.first_name = first_name
        self.last_name = last_name
        self.pin = pin
        self.balance = balance
        self.transaction_history = []

    def check_balance(self):
        return self.balance

    def withdraw(self, amount):
        if amount > self.balance:
            return False
        else:
            self.balance -= amount
            self.transaction_history.append(f"Withdrawal: ${amount:.2f}")
            return True

    def deposit(self, amount):
        self.balance += amount
        self.transaction_history.append(f"Deposit: ${amount:.2f}")

    def show_transaction_history(self):
        return self.transaction_history

class BankingApp(QMainWindow):
    def __init__(self):
        super(BankingApp, self).__init__()
        uic.loadUi("home.ui", self)  # Load the UI file

        # Connect signals to slots
        self.loginButton.clicked.connect(self.login)
        self.registerButton.clicked.connect(self.show_register)
        self.depositButton.clicked.connect(self.deposit)
        self.withdrawButton.clicked.connect(self.withdraw)
        self.historyButton.clicked.connect(self.show_history)
        self.logoutButton.clicked.connect(self.logout)

        self.current_user = None

    def login(self):
        first_name = self.firstNameInput.text()
        last_name = self.lastNameInput.text()
        pin = self.pinInput.text()
        user_key = f"{first_name.lower()}_{last_name.lower()}"
        if user_key in users and users[user_key].pin == pin:
            self.current_user = users[user_key]
            self.show_dashboard()
        else:
            self.show_error("Invalid credentials. Please try again.")

    def show_register(self):
        first_name = self.firstNameInput.text()
        last_name = self.lastNameInput.text()
        pin = self.pinInput.text()
        user_key = f"{first_name.lower()}_{last_name.lower()}"
        if user_key not in users:
            users[user_key] = User(first_name, last_name, pin)
            self.show_success("Registration successful. You can now log in.")
        else:
            self.show_error("User already exists.")

    def show_dashboard(self):
        self.stackedWidget.setCurrentWidget(self.dashboardPage)
        self.update_balance()

    def update_balance(self):
        self.balanceLabel.setText(f"Balance: ${self.current_user.check_balance():.2f}")

    def deposit(self):
        amount = float(self.amountInput.text())
        self.current_user.deposit(amount)
        self.update_balance()

    def withdraw(self):
        amount = float(self.amountInput.text())
        if not self.current_user.withdraw(amount):
            self.show_error("Insufficient funds.")
        self.update_balance()

    def show_history(self):
        history = "\n".join(self.current_user.show_transaction_history())
        QMessageBox.information(self, "Transaction History", history)

    def logout(self):
        self.current_user = None
        self.stackedWidget.setCurrentWidget(self.homePage)

    def show_error(self, message):
        QMessageBox.critical(self, "Error", message)

    def show_success(self, message):
        QMessageBox.information(self, "Success", message)


if __name__ == '__main__':
    app = QApplication([])
    window = BankingApp()
    window.show()
    app.exec_()
