import sqlite3
import os
import requests

DB_FILE = os.path.join(os.path.dirname(__file__), "db/contacts.db")
SQL_FILE= os.path.join(os.path.dirname(__file__), "contacts.sql")
IMAGES_DIR= os.path.join(os.path.dirname(__file__), "db/images")

def check_db():
    if os.path.isfile(DB_FILE):
        print(f"Using existing {DB_FILE} database.")
        return

    print(f"{DB_FILE} not found. Creating database from {SQL_FILE}...")
    if not os.path.exists(SQL_FILE):
        print("Error: SQL file not found.")
        exit()

    conn = sqlite3.connect(DB_FILE)
    with open(SQL_FILE, "r") as f: 
        sql = f.read()
        conn.executescript(sql)

    # Getting people's names
    cursor = conn.execute("SELECT name FROM contacts;")
    result = cursor.fetchall()
    names = [x[0].lower() for x in result]
    conn.close()

    for name in names:
        url = f'https://robohash.org/{name}'
        response = requests.get(url)

        if response.status_code == 200:
            filename = f'{name}.png'
            filepath = os.path.join(IMAGES_DIR, filename)

            with open(filepath, 'wb') as f:
                f.write(response.content)
                print(f'Saved image for {name} at {filepath}')
