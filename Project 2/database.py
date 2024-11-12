# database.py
import sqlite3
from datetime import datetime

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
                        target_audience TEXT,
                        date_created TEXT NOT NULL
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
    date_created = datetime.now().isoformat()  # Get current date and time in ISO 8601 format
    cursor.execute('''INSERT INTO business_plans (username, business_name, description, goals, target_audience, date_created)
                      VALUES (?, ?, ?, ?, ?, ?)''',
                   (username, business_name, description, goals, target_audience, date_created))
    conn.commit()
    conn.close()

def update_business_plan(original_business_name, new_business_name, description, goals, target_audience):
    """Update an existing business plan"""
    conn = sqlite3.connect("thunder.db")
    try:
        cursor = conn.cursor()
        date_updated = datetime.now().isoformat() 
        cursor.execute(""" 
            UPDATE business_plans 
            SET business_name = ?, description = ?, goals = ?, target_audience = ?, date_created = ?
            WHERE business_name = ?
        """, (new_business_name, description, goals, target_audience, date_updated, original_business_name))
        conn.commit()
        print(f"Business plan '{original_business_name}' updated to '{new_business_name}' successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred while updating the business plan: {e}")
    finally:
        conn.close()

def check_business_name_exists(business_name):
    """Check if a business name already exists"""
    conn = sqlite3.connect("thunder.db")
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM business_plans WHERE business_name = ?", (business_name,))
        exists = cursor.fetchone()[0] > 0
        return exists
    except sqlite3.Error as e:
        print(f"An error occurred while checking business name: {e}")
        return False
    finally:
        conn.close()

def get_business_plan_data(username, business_name):
    """Fetch the business plan data from the database for the given username and business_name."""
    connection = sqlite3.connect("thunder.db") 
    cursor = connection.cursor()
    
    query = """
    SELECT description, goals, target_audience
    FROM business_plans
    WHERE username = ? AND business_name = ?
    """
    cursor.execute(query, (username, business_name))
    
    result = cursor.fetchone()  
    
    connection.close()
    
    if result:
        return result  
    else:
        return None          