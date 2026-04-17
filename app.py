from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os
import requests
from werkzeug.security import generate_password_hash, check_password_hash
from config import EXCHANGE_API_KEY
from ml.forecast import get_forecast

app = Flask(__name__)
app.secret_key = 'expensetracker2026'
DATABASE = 'database.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def convert_to_inr(amount, currency):
    if currency == 'INR':
        return amount
    try:
        url = f'https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}/pair/{currency}/INR/{amount}'
        response = requests.get(url)
        data = response.json()
        if data['result'] == 'success':
            return round(data['conversion_result'], 2)
    except:
        pass
    return amount

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            note TEXT,
            tag TEXT,
            date TEXT NOT NULL,
            currency TEXT DEFAULT 'INR',
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    conn.close()

# ── Login ──
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        name = request.form['name'].strip()
        password = request.form['password'].strip()
        if name and password:
            conn = get_db()
            user = conn.execute('SELECT * FROM users WHERE name = ?', (name,)).fetchone()
            if user:
                # existing user — check password
                if check_password_hash(user['password'], password):
                    session['user_id'] = user['id']
                    session['user_name'] = user['name']
                    conn.close()
                    return redirect(url_for('index'))
                else:
                    error = 'Wrong password! Try again.'
            else:
                # new user — create account
                hashed = generate_password_hash(password)
                conn.execute('INSERT INTO users (name, password) VALUES (?, ?)', (name, hashed))
                conn.commit()
                user = conn.execute('SELECT * FROM users WHERE name = ?', (name,)).fetchone()
                session['user_id'] = user['id']
                session['user_name'] = user['name']
                conn.close()
                return redirect(url_for('index'))
    return render_template('login.html', error=error)

# ── Dashboard ──
@app.route('/dashboard')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db()
    expenses = conn.execute(
        'SELECT * FROM expenses WHERE user_id = ? ORDER BY date DESC',
        (session['user_id'],)
    ).fetchall()
    conn.close()
    return render_template('index.html', expenses=expenses)

# ── Add Expense ──
@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        amount = float(request.form['amount'])
        category = request.form['category']
        note = request.form['note']
        tag = request.form['tag']
        date = request.form['date']
        currency = request.form['currency']
        converted_amount = convert_to_inr(amount, currency)
        conn = get_db()
        conn.execute(
            'INSERT INTO expenses (user_id, amount, category, note, tag, date, currency) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (session['user_id'], converted_amount, category, note, tag, date, 'INR')
        )
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_expense.html')

# ── Report ──
@app.route('/report', methods=['GET', 'POST'])
def report():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    budget = 10000
    if request.method == 'POST':
        budget = float(request.form['budget'])
    data = get_forecast(session['user_id'], budget)
    return render_template('report.html',
        predicted=data['predicted'],
        spent_so_far=data['spent_so_far'],
        budget=data['budget'],
        alert=data['alert'],
        predictions=data['predictions']
    )

# ── Logout ──
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ── Delete Expense ──
@app.route('/delete/<int:expense_id>')
def delete_expense(expense_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db()
    conn.execute(
        'DELETE FROM expenses WHERE id = ? AND user_id = ?',
        (expense_id, session['user_id'])
    )
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)