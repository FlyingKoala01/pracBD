"""
==================
This module is used to create to handle the DB. Its creation and import/export of its contents into a CSV file
==================
"""

import sqlite3
import csv
import os 

DB_FILE = "employees.db"
SQL_FILE = "employees.sql"
CSV_FILE = "employees.csv"

def check_db():
    """
    Checks if the database file exists, if not, it checks for an SQL file to be used to create the database
    """
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

def dump_db():
    """
    Function used to create a folder with the .csv files containing all the information from the different tables
    """
    dir_name = "csv_files"
    os.makedirs(dir_name, exist_ok=True)
    with sqlite3.connect(DB_FILE) as conn:
        tables = ["employee", "job", "company", "manager"]
        for table in tables:
            file_path = os.path.join(dir_name, f"{table}.csv")
            with open(file_path, "w", newline="") as file:
                writer = csv.writer(file)
                cursor = conn.execute(f"SELECT * FROM {table}")
                writer.writerow([description[0] for description in cursor.description])
                writer.writerows(cursor)

def load_db():
    """
    Reads the contents of each csv file inside the folder created with the function `dumb_db()`. ALl the contents 
    from the files are saved in the database.
    """
    with sqlite3.connect(DB_FILE) as conn:
        tables = ["employee", "job", "company", "manager"]
        for table in tables:
            file_path = os.path.join("csv_files", f"{table}.csv")
            with open(file_path, newline="") as file:
                reader = csv.reader(file)
                headers = next(reader)
                query = f"INSERT INTO {table} ({', '.join(headers)}) VALUES ({', '.join('?' * len(headers))})"
                conn.executemany(query, reader)
        conn.commit()