import sqlite3
import os

DB_NAME = 'bank.db'

def initialize_database():
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
        print(f"Existing {DB_NAME} deleted.")
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE accounts (
        account_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        balance REAL DEFAULT 0.0
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE transactions (
        transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_id INTEGER,
        transaction_type TEXT NOT NULL,
        amount REAL NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (account_id) REFERENCES accounts (account_id)
    )
    ''')
    
    conn.commit()
    conn.close()
    print(f"Database {DB_NAME} initialized successfully.")

if __name__ == "__main__":
    initialize_database()