import sqlite3

def init_db():
    conn = sqlite3.connect('funds.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS batting_averages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fund_name TEXT NOT NULL,
            benchmark_name TEXT NOT NULL,
            average REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_batting_average(fund_name, benchmark_name, average):
    conn = sqlite3.connect('funds.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO batting_averages (fund_name, benchmark_name, average)
        VALUES (?, ?, ?)
    ''', (fund_name, benchmark_name, average))
    conn.commit()
    conn.close()


def get_batting_averages():
    conn = sqlite3.connect('funds.db')
    c = conn.cursor()
    c.execute('SELECT * FROM batting_averages')
    rows = c.fetchall()
    conn.close()
    return rows
