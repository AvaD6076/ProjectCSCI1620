from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

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


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        pin = request.form['pin']
        user_key = f"{first_name.lower()}_{last_name.lower()}"
        if user_key in users and users[user_key].pin == pin:
            session['user'] = user_key
            return redirect(url_for('dashboard'))
        else:
            return render_template('index.html', error="Invalid credentials. Please try again.")
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        pin = request.form['pin']
        user_key = f"{first_name.lower()}_{last_name.lower()}"
        if user_key not in users:
            users[user_key] = User(first_name, last_name, pin)
            return redirect(url_for('home'))
        else:
            return render_template('register.html', error="User already exists.")
    return render_template('register.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user' not in session:
        return redirect(url_for('home'))
    
    user = users[session['user']]

    if request.method == 'POST':
        if 'withdraw' in request.form:
            amount = float(request.form['amount'])
            if not user.withdraw(amount):
                return render_template('dashboard.html', user=user, error="Insufficient funds.")
        elif 'deposit' in request.form:
            amount = float(request.form['amount'])
            user.deposit(amount)
    
    return render_template('dashboard.html', user=user)


@app.route('/history')
def history():
    if 'user' not in session:
        return redirect(url_for('home'))

    user = users[session['user']]
    return render_template('history.html', user=user)


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
