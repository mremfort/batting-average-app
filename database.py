import sqlite3
import shutil
import os

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

# Remove a record from the fund_scores table
def remove_score(fund_name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM fund_scores WHERE fund_name = ?', (fund_name,))
    conn.commit()
    conn.close()

# Backup the database
def backup_database():
    if not os.path.exists('backups'):
        os.makedirs('backups')
    
    # Get the list of existing backups
    backups = sorted([f for f in os.listdir('backups') if f.startswith('funds_scores_backup_')])
    
    # Remove the oldest backup if there are already 5 backups
    if len(backups) >= 5:
        os.remove(os.path.join('backups', backups[0]))
    
    # Create a new backup
    backup_filename = f'funds_scores_backup_{len(backups) + 1}.db'
    shutil.copy('funds_scores.db', os.path.join('backups', backup_filename))
