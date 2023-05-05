
import sqlite3

from os import path

PROJECT_ABS_PATH = path.dirname(path.abspath(__file__))
DB_FILE_PATH = f"{PROJECT_ABS_PATH}/contacts.db"


def commit_and_close(func):
    """
    A decorator used to add basic SQLlite requirements for most queries. Eliminates code-repetition from module.
    The decorator connects to the DB before executing any query. Commits the query, closes the DB and returns the result.
    """
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect(DB_FILE_PATH)
        conn.execute("PRAGMA foreign_keys=ON;")
        try:
            result = func(conn, *args, **kwargs)
        except sqlite3.IntegrityError:
            print("ERROR: Integrity Error.\n You may have referenced a non-existent ID or you may have tried to add an already existent primary ID.")    
            return
        except sqlite3.OperationalError:
            print("ERROR: Column not found. Make sure you spelled the column's name correctly.")
            return
        conn.commit()
        conn.close()
        return result
    return wrapper


@commit_and_close
def modify_phone(conn, name, phone):
    query = f"UPDATE contacts SET phone_number = ? WHERE name = ?;"
    conn.execute(query, (phone, name,))

@commit_and_close
def modify_name(conn, name, new_name):
    query = f"UPDATE contacts SET name = ? WHERE name = ?;"
    conn.execute(query, (new_name, name,))

@commit_and_close
def delete_contact(conn, name):
    query = f"DELETE FROM contacts WHERE name = ?;"
    conn.execute(query, (name,))

@commit_and_close
def show_contacts(conn):
    cursor = conn.execute("SELECT * FROM contacts;")
    result = cursor.fetchall()
    return result

@commit_and_close
def insert_contact(conn, name, phone,):
    query = f"INSERT INTO contacts (name, phone_number) VALUES (?, ?);"
    conn.execute(query, (name, phone,))