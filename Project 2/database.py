# database.py
import sqlite3

# Database connection and table setup
def initialize_db():
    conn = sqlite3.connect("thunder.db")
    cursor = conn.cursor()

    # Create users table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Create the table with an additional column for the username
    cursor.execute('''CREATE TABLE IF NOT EXISTS business_plans (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        business_name TEXT NOT NULL,
                        description TEXT,
                        goals TEXT,
                        target_audience TEXT
                    )''')
    conn.commit()
    conn.close()

def create_user(username, password):
    conn = sqlite3.connect('thunder.db')
    cursor = conn.cursor()
    
    # Insert user data
    sql = "INSERT INTO users (username, password) VALUES (?, ?)"
    val = (username, password)
    
    try:
        cursor.execute(sql, val)
        conn.commit()
        print(f"User {username} created successfully.")
    except sqlite3.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# Update the insert function to accept a username
def insert_business_plan(username, business_name, description, goals, target_audience):
    conn = sqlite3.connect("thunder.db")
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO business_plans (username, business_name, description, goals, target_audience)
                      VALUES (?, ?, ?, ?, ?)''',
                   (username, business_name, description, goals, target_audience))
    conn.commit()
    conn.close()
