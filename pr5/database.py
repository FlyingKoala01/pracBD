
import sqlite3
#import csv
import os 


DB_FILE = "contacts.db"
SQL_FILE= "contacts.sql"

def check_db():
    if not os.path.isfile(DB_FILE):
        print(f"{DB_FILE} not found. Creating database from {SQL_FILE}...")
        if not os.path.exists(SQL_FILE):
            print("Error: SQL file not found.")
            exit()

        conn = sqlite3.connect(DB_FILE)
        with open(SQL_FILE, "r") as f: 
            sql = f.read()
            conn.executescript(sql)
        conn.close()
    else:
        print(f"Using existing {DB_FILE} database.")