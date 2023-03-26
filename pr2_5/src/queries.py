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
        conn.execute("PRAGMA foreign_keys=ON;")
        try:
            result = func(conn, *args, **kwargs)
        except sqlite3.IntegrityError:
            print("ERROR: Before you register a job or a manager, make sure the given employee(s) ID and/or the company ID are registered.")    
            return
        except sqlite3.OperationalError:
            print("Column not found. Make sure you spelled the column's name correctly.")
            return
        conn.commit()
        conn.close()
        return result
    return wrapper

@commit_and_close
def check_employee(conn, id_employee):
    cursor = conn.execute("SELECT COUNT(*) FROM employee WHERE id_employee = ?", (id_employee,))
    result = cursor.fetchone()[0]
    return result

@commit_and_close
def check_company(conn, id_company):
    cursor = conn.execute("SELECT COUNT(*) FROM company WHERE id_company = ?", (id_company,))
    result = cursor.fetchone()[0]
    return result

@commit_and_close
def check_job(conn, id_employee):
    cursor = conn.execute("SELECT COUNT(*) FROM job WHERE id_employee = ?", (id_employee,))
    result = cursor.fetchone()[0]
    return result

@commit_and_close
def check_manager(conn, id_employee):
    cursor = conn.execute("SELECT COUNT(*) FROM manager WHERE id_employee = ?", (id_employee,))
    result = cursor.fetchone()[0]
    return result


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
    conn.execute("DELETE FROM company WHERE id_company = ?", (id_company,))

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

@commit_and_close
def view_employee(conn):
    cursor = conn.execute("SELECT * FROM employee")
    return cursor.fetchall()

@commit_and_close
def view_job(conn):
    cursor = conn.execute("SELECT * FROM job")
    return cursor.fetchall()

@commit_and_close
def view_company(conn):
    cursor = conn.execute("SELECT * FROM company")
    return cursor.fetchall()

@commit_and_close
def view_manager(conn):
    cursor = conn.execute("SELECT * FROM manager")
    return cursor.fetchall()

@commit_and_close
def company_with_most_employees(conn):
    query = "SELECT id_company, COUNT(id_employee) AS total_employees\
            FROM job\
            GROUP BY id_company\
            ORDER BY total_employees DESC\
            LIMIT 1;"
    cursor = conn.execute(query)
    return cursor.fetchall()

@commit_and_close
def update_managers_salary(conn, increase_factor):
    query = "UPDATE job\
            SET salary = salary * ?\
            WHERE id_employee IN (\
            SELECT id_employee_coordinator\
            FROM manager);"
    conn.execute(query, (increase_factor,))

@commit_and_close
def employees_same_city(conn):
    query = "SELECT id_employee\
            FROM employee\
            WHERE city = (\
                SELECT city\
                FROM company\
                WHERE id_company = (\
                    SELECT id_company\
                    FROM (\
                        SELECT id_employee, id_company\
                        FROM job\
                    ) AS job_employee\
                    WHERE job_employee.id_employee = employee.id_employee\
                ));"
    cursor = conn.execute(query)
    return cursor.fetchall()

@commit_and_close
def employees_in_city(conn, city):
    query = f"SELECT id_employee FROM employee WHERE city = ?"
    cursor = conn.execute(query, (city,))
    return cursor.fetchall()

@commit_and_close
def employees_by_salary(conn, order):
    if order == "asc":
        query = f"SELECT id_employee FROM job WHERE id_employee IN (SELECT id_employee FROM employee) ORDER BY salary ASC;"
    else:
        query = f"SELECT id_employee FROM job WHERE id_employee IN (SELECT id_employee FROM employee) ORDER BY salary DESC;"
    cursor = conn.execute(query)
    return cursor.fetchall()