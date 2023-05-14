import sqlite3, shutil
from os import path, remove
from database import DB_FILE


_images = path.join(path.dirname(__file__), "db/images")
PROJECT_ABS_PATH = path.dirname(path.abspath(__file__))


def commit_and_close(func):
    """
    A decorator used to add basic SQLlite requirements for most queries. Eliminates code-repetition from module.
    The decorator connects to the DB before executing any query. Commits the query, closes the DB and returns the result.
    """
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect(DB_FILE)
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

def copy_to_db(filepath):
    """
    Given a filename of an existing photo, it copies it into /db/images.
    It checks that we're not overriding any existing file by adding (n).
    Returns the new filename.
    """
    filename = path.basename(filepath)
    name, ext = path.splitext(filename)
    dest_path = path.join(_images, filename)
    i = 1
    while path.exists(dest_path):
        filename = f"{name}_{i}{ext}"
        dest_path = path.join(_images, filename)
        i += 1
    shutil.copy(filepath, dest_path)
    return path.basename(dest_path)

def delete_image_if_exists(conn, id):
    cursor = conn.execute("SELECT filename FROM contacts WHERE id = ?;", (id,))
    filename = cursor.fetchall()[0][0]
    if filename != None:
        remove(path.join(_images, filename))

@commit_and_close
def modify_phone(conn, id, phone):
    query = f"UPDATE contacts SET phone_number = ? WHERE id = ?;"
    conn.execute(query, (phone, id,))

@commit_and_close
def modify_name(conn, id, new_name):
    query = f"UPDATE contacts SET name = ? WHERE id = ?;"
    conn.execute(query, (new_name, id,))

@commit_and_close
def delete_contact(conn, id):
    delete_image_if_exists(conn, id)
    query = f"DELETE FROM contacts WHERE id = ?;"
    conn.execute(query, (id,))

@commit_and_close
def show_contacts(conn):
    cursor = conn.execute("SELECT * FROM contacts;")
    result = cursor.fetchall()
    return result

@commit_and_close
def insert_contact(conn, name, phone, filename):
    if filename != None:
        new_filename = copy_to_db(filename)
        query = f"INSERT INTO contacts (name, phone_number, filename) VALUES (?, ?, ?);"
        conn.execute(query, (name, phone, new_filename,))
    else:
        query = f"INSERT INTO contacts (name, phone_number) VALUES (?, ?);"
        conn.execute(query, (name, phone,))

@commit_and_close
def get_image_from_id(conn, contact_id):
    cursor = conn.execute("SELECT filename FROM contacts WHERE id = ?;", (contact_id,))
    result = cursor.fetchall()
    return result[0][0]

@commit_and_close
def exists(conn, name, telf):
    cursor = conn.execute("SELECT * FROM contacts WHERE name = ? AND phone_number = ?;", (name, telf,))
    result = cursor.fetchall()
    return len(result) != 0

@commit_and_close
def modify_image(conn, id, filename):
    delete_image_if_exists(conn, id)
    new_filename = copy_to_db(filename)
    query = f"UPDATE contacts SET filename = ? WHERE id = ?;"
    conn.execute(query, (new_filename, id,))
