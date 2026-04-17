import sqlite3
import pandas as pd
import os

def load_data(user_id):
    db_path = os.path.join(os.path.dirname(__file__), '..', 'database.db')
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(
        "SELECT * FROM expenses WHERE user_id = ?",
        conn,
        params=(user_id,)
    )
    conn.close()
    return df

def preprocess(user_id):
    df = load_data(user_id)

    if df.empty:
        return None, 0

    # Convert date column to datetime
    df['date'] = pd.to_datetime(df['date'])

    # Extract day of month as a number
    df['day'] = df['date'].dt.day

    # Group by day — sum all expenses on same day
    daily = df.groupby('day')['amount'].sum().reset_index()
    daily.columns = ['day', 'total']

    # Total spent so far
    spent_so_far = round(df['amount'].sum(), 2)

    return daily, spent_so_far