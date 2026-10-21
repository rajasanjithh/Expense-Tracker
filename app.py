import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-only-change-this-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'  # Database file will be named expenses.db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User model for the database
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Create the database (run once)
with app.app_context():
    db.create_all()

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/index')
def index():
    return render_template('index.html')


# Register page
@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'error')
            return redirect(url_for('register'))
        
        # Create a new user and add to the database
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if user exists and password matches
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        
        flash('Invalid credentials. Please try again.', 'error')
    
    return render_template('login.html')

# Logout page
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)




# Expense list to store expenses
expenses = [
    {'amount': 50, 'category': 'Food', 'description': 'Grocery shopping', 'date': '2024-12-25'},
    {'amount': 20, 'category': 'Transport', 'description': 'Bus fare', 'date': '2024-12-24'},
    {'amount': 100, 'category': 'Entertainment', 'description': 'Movie night', 'date': '2024-12-22'}
]

# Route to display the home page (Expense Tracker)

# Route to handle form submission (Add or Update Expense)
@app.route('/add', methods=['POST'])
def add_expense():
    amount = request.form['amount']
    category = request.form['category']
    description = request.form['description']
    date = request.form['date']

    # Add the new expense to the expenses list
    expenses.insert(0, {'amount': amount, 'category': category, 'description': description, 'date': date})
    
    return redirect(url_for('index'))

# Route to handle expense editing
@app.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit_expense(index):
    if request.method == 'POST':
        amount = request.form['amount']
        category = request.form['category']
        description = request.form['description']
        date = request.form['date']

        # Update the expense at the specified index
        expenses[index] = {'amount': amount, 'category': category, 'description': description, 'date': date}
        return redirect(url_for('index'))
    
    # Pre-fill the form with the selected expense data for editing
    expense = expenses[index]
    return render_template('edit.html', expense=expense, index=index)

# Route to handle expense deletion
@app.route('/delete/<int:index>', methods=['GET'])
def delete_expense(index):
    # Remove the expense from the list
    expenses.pop(index)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
