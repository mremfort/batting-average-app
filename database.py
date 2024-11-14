import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
def connect_db():
    conn = sqlite3.connect('funds_scores.db')
    return conn

# Create a table to store fund scores
def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fund_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fund_name TEXT UNIQUE,
            benchmark_name TEXT,
            benchmark_ticker TEXT,
            general_comparison_average REAL,
            up_benchmark_average REAL,
            down_benchmark_average REAL
        )
    ''')
    conn.commit()
    conn.close()

# Insert or update a record in the fund_scores table
def insert_or_update_score(fund_name, benchmark_name, benchmark_ticker, general_comparison_average, up_benchmark_average, down_benchmark_average):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO fund_scores (fund_name, benchmark_name, benchmark_ticker, general_comparison_average, up_benchmark_average, down_benchmark_average)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(fund_name) DO UPDATE SET
            benchmark_name=excluded.benchmark_name,
            benchmark_ticker=excluded.benchmark_ticker,
            general_comparison_average=excluded.general_comparison_average,
            up_benchmark_average=excluded.up_benchmark_average,
            down_benchmark_average=excluded.down_benchmark_average
    ''', (fund_name, benchmark_name, benchmark_ticker, general_comparison_average, up_benchmark_average, down_benchmark_average))
    conn.commit()
    conn.close()

# Fetch all records from the fund_scores table
def fetch_scores():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM fund_scores')
    rows = cursor.fetchall()
    conn.close()
    return rows
