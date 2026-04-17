# Smart Expense Tracker 

ML-Powered Personal Finance Web Application built with Flask and SQLite.

## Features
- Multi-user login with password
- Add expenses with voice input
- Real-time currency conversion (INR default)
- ML Linear Regression budget forecasting
- Interactive Chart.js dashboard
- Budget overspend alert

## Tech Stack
- Python, Flask, SQLite
- scikit-learn, Pandas, NumPy
- Bootstrap 5, Chart.js
- Web Speech API, ExchangeRate-API

## Setup Instructions
1. Clone the repo: `git clone https://github.com/YOURUSERNAME/smart-expense-tracker`
2. Create virtual environment: `python -m venv venv`
3. Activate: `venv\Scripts\activate`
4. Install packages: `pip install -r requirements.txt`
5. Create `config.py` and add: `EXCHANGE_API_KEY = 'your_key_here'`
6. Run: `python app.py`
7. Open: `http://127.0.0.1:5000`
