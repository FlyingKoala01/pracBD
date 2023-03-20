"""
==================

This module contains all of the possible queries available to the user. 
Having hard-coded and ease-to-use queries makes the main module more readable and simple to expand.

The purpose of each query should be self-explanatory thanks to its name.

==================
"""

import sqlite3

from os import path

PROJECT_ABS_PATH = path.dirname(path.abspath(__file__))
DB_FILE_PATH = f"{PROJECT_ABS_PATH}/employees.db"

def commit_and_close(func):
    """
    A decorator used to add basic SQLlite requirements for most queries. Eliminates code-repetition from module
    """
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect(DB_FILE_PATH)
        result = func(conn, *args, **kwargs)
        conn.commit()
        conn.close()
        return result
    return wrapper

@commit_and_close
def insert_employee(conn, id_employee, street, city):
    conn.execute("INSERT INTO employee (id_employee, street, city) VALUES (?, ?, ?)", (id_employee, street, city))

@commit_and_close
def insert_job(conn, id_employee, id_company, salary):
    conn.execute("INSERT INTO job (id_employee, id_company, salary) VALUES (?, ?, ?)", (id_employee, id_company, salary))

@commit_and_close
def insert_company(conn, id_company, city):
    conn.execute("INSERT INTO company (id_company, city) VALUES (?, ?)", (id_company, city))

@commit_and_close
def insert_manager(conn, id_employee, id_employee_coordinator):
    conn.execute("INSERT INTO manager (id_employee, id_employee_coordinator) VALUES (?, ?)", (id_employee, id_employee_coordinator))

@commit_and_close
def delete_employee(conn, id_employee):
    conn.execute("DELETE FROM employee WHERE id_employee = ?", (id_employee,))

@commit_and_close
def delete_job(conn, id_employee):
    conn.execute("DELETE FROM job  WHERE id_employee = ? ", (id_employee,))

@commit_and_close
def delete_company(conn, id_company):
    conn.execute("DELETE FROM company WHERE id = ?", (id_company,))

@commit_and_close
def delete_manager(conn, id_employee):
    conn.execute("DELETE FROM manager WHERE id_employee = ?", (id_employee,))

@commit_and_close
def modify_employee(conn, id_employee, col, value):
    query = f"UPDATE employee SET {col} = ? WHERE id_employee = ?"
    conn.execute(query, (value, id_employee))


@commit_and_close
def modify_job(conn, id_employee, col, value):
    query = f"UPDATE job SET {col} = ? WHERE id_employee = ?"
    conn.execute(query, (value, id_employee))


@commit_and_close
def modify_company(conn, id_company, col, value):
    query = f"UPDATE company SET {col} = ? WHERE id_company = ?"
    conn.execute(query, (value, id_company))


@commit_and_close
def modify_manager(conn, id_employee, col, id_employee_coordinator):
    query = f"UPDATE manager SET {col} = ? WHERE id_employee = ?"
    conn.execute(query, (id_employee, id_employee_coordinator))

def view_employee():
    conn = sqlite3.connect(DB_FILE_PATH)
    cursor = conn.execute("SELECT * FROM employee")
    return cursor.fetchall()

def view_job():
    conn = sqlite3.connect(DB_FILE_PATH)
    cursor = conn.execute("SELECT * FROM job")
    return cursor.fetchall()

def view_company():
    conn = sqlite3.connect(DB_FILE_PATH)
    cursor = conn.execute("SELECT * FROM company")
    return cursor.fetchall()

def view_manager():
    conn = sqlite3.connect(DB_FILE_PATH)
    cursor = conn.execute("SELECT * FROM manager")
    return cursor.fetchall()
