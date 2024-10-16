import mysql.connector

def create_user(username, password):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Corrected the typo here
        database="thunder"
    )
    
    cursor = conn.cursor()
    
    # Insert user data
    sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
    val = (username, password)
    
    try:
        cursor.execute(sql, val)
        conn.commit()
        print(f"User {username} created successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()
