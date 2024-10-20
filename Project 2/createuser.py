import sqlite3

def create_user(username, password):
    conn = sqlite3.connect('thunder.db')
    cursor = conn.cursor()
    
    # Create users table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

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
