# database.py
import sqlite3
import sys
import os
from datetime import datetime

# Database connection and table setup
def initialize_db():
    """Initialize the database."""
    conn = sqlite3.connect("thunder.db")
    cursor = conn.cursor()

    # Create users table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            username TEXT UNIQUE NOT NULL,
            password TEXT,
            google_id TEXT UNIQUE,
            sign_in_count INTEGER DEFAULT 0,
            last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            login_timestamp TEXT NOT NULL,
            logout_timestamp TEXT NOT NULL,
            pushed TEXT DEFAULT 'N'
        )
    ''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS business_plans (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        business_name TEXT NOT NULL,
                        industry TEXT,
                        num_employees TEXT,
                        legal_structure TEXT,
                        date_created TEXT NOT NULL,
                        percentage REAL
                    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS executive_summary (
                        username TEXT NOT NULL,
                        business_name TEXT NOT NULL,
                        description TEXT,
                        mission_statement TEXT,
                        principal_members TEXT,
                        future TEXT,
                        FOREIGN KEY (username, business_name) REFERENCES business_plans (username, business_name)
                    )
                    ''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS market_research (
                        username TEXT NOT NULL,
                        business_name TEXT NOT NULL,
                        industry TEXT,
                        competitors TEXT,
                        target_audience TEXT,
                        company_advantages TEXT,
                        regulations TEXT,
                        FOREIGN KEY (username, business_name) REFERENCES business_plans (username, business_name)
                    )
                    ''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS marketing_strategy (
                        username TEXT NOT NULL,
                        business_name TEXT NOT NULL,
                        growth_strategy TEXT,
                        advertising TEXT,
                        marketing_budget TEXT,
                        customer_interaction TEXT,
                        customer_retention TEXT,
                        FOREIGN KEY (username, business_name) REFERENCES business_plans (username, business_name)
                    )
                    ''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS service_line (
                        username TEXT NOT NULL,
                        business_name TEXT NOT NULL,
                        products TEXT,
                        services TEXT,
                        pricing_structure TEXT,
                        research_development TEXT,
                        FOREIGN KEY (username, business_name) REFERENCES business_plans (username, business_name)
                    )
                    ''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS contact_information (
                        username TEXT NOT NULL,
                        business_name TEXT NOT NULL,
                        contact_name TEXT,
                        address TEXT,
                        city TEXT,
                        state TEXT,
                        zip TEXT,
                        phone TEXT,
                        email TEXT,
                        FOREIGN KEY (username, business_name) REFERENCES business_plans (username, business_name)
                    )
                    ''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS financial (
                        username TEXT NOT NULL,
                        business_name TEXT NOT NULL,
                        financing_sought TEXT,
                        profit_loss_statement TEXT,
                        break_even_analysis TEXT,
                        return_on_investment TEXT,
                        contingency_plan TEXT, 
                        disaster_recovery TEXT,
                        bank TEXT,
                        accounting_firm TEXT,
                        insurance_info TEXT, 
                        FOREIGN KEY (username, business_name) REFERENCES business_plans (username, business_name)
                    )
                    ''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS legal (
                        username TEXT NOT NULL,
                        business_name TEXT NOT NULL,
                        intellectual_property TEXT,
                        law_firm TEXT,
                        FOREIGN KEY (username, business_name) REFERENCES business_plans (username, business_name)
                    )
                    ''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS revenue_projection (
                        username TEXT NOT NULL,
                        business_name TEXT NOT NULL, 
                        year INTEGER NOT NULL,
                        revenue INTEGER NOT NULL,
                        expenditure INTEGER NOT NULL,
                        FOREIGN KEY (username, business_name) REFERENCES business_plans (username, business_name)
                        )
                    ''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS market_analysis (
                        username TEXT NOT NULL,
                        business_name TEXT NOT NULL,
                        competitor TEXT NOT NULL,
                        market_share INTEGER NOT NULL,
                        FOREIGN KEY (username, business_name) REFERENCES business_plans (username, business_name)
                    )
                ''')

    conn.commit()
    conn.close()

def create_user(username, password):
    """Create a new user in the databse."""
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

def insert_business_plan(username, data):
    """Insert a new business plan"""
    conn = sqlite3.connect("thunder.db")
    cursor = conn.cursor()
    try:
        # Insert into business_plans table
        print("Business plans")
        cursor.execute('''
            INSERT INTO business_plans (username, business_name, industry, num_employees, legal_structure, date_created, percentage)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            username,
            data["business_name"],
            data["industry"],
            data["employees"],
            data["legal_structure"],
            datetime.now().isoformat(),
            data["percentage"]
        ))

        print("Executive Summary")
        cursor.execute('''
            INSERT INTO executive_summary (username, business_name, description, mission_statement, principal_members, future)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            username,
            data["business_name"],
            data["description"],
            data["mission_statement"],
            data["principal_members"],
            data["future"]
        ))

        print("Market Research")
        cursor.execute('''
            INSERT INTO market_research (username, business_name, industry, competitors, target_audience, company_advantages, regulations)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            username,
            data["business_name"],
            data["industry_state"],
            data["competitors"],
            data["target_audience"],
            data["company_advantages"],
            data["regulations_compliance"]
        ))

        print("Marketing Srategy")
        cursor.execute('''
            INSERT INTO marketing_strategy (username, business_name, growth_strategy, advertising, marketing_budget, customer_interaction, customer_retention)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            username,
            data["business_name"],
            data["growth_strategy"],
            data["advertising_plan"],
            data["marketing_budget"],
            data["customer_interaction"],
            data["customer_retention"]
        ))

        print("Service Line")
        cursor.execute('''
            INSERT INTO service_line (username, business_name, products, services, pricing_structure, research_development)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            username,
            data["business_name"],
            data["products"],
            data["services"],
            data["pricing"],
            data["research"]
        ))

        print("Contact Info")
        cursor.execute('''
            INSERT INTO contact_information (username, business_name, contact_name, address, city, state, zip, phone, email)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            username,
            data["business_name"],
            data["contact_name"],
            data["address"],
            data["city"],
            data["state"],
            data["zip_code"],
            data["phone"],
            data["email"],
        ))

        print("Financial")
        cursor.execute('''
            INSERT INTO financial (username, business_name, financing_sought, profit_loss_statement, break_even_analysis, return_on_investment, contingency_plan, disaster_recovery, bank, accounting_firm, insurance_info)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            username,
            data["business_name"],
            data["financing_sought"],
            data["profit_loss_statement"],
            data["break_even_analysis"],
            data["roi"],
            data["contingency_plan"],
            data["disaster_recovery_plan"],
            data["bank"],
            data["accounting_firm"],
            data["insurance_info"]
        ))

        print("Legal")
        cursor.execute('''
            INSERT INTO legal (username, business_name, intellectual_property, law_firm)
            VALUES (?, ?, ?, ?)
        ''', (
            username,
            data["business_name"],
            data["intellectual_property"],
            data["law_firm"]
        ))

        print("Revenue")
        # Insert revenue projections into revenue_projection table
        for projection in data["revenue_projection"]:
            cursor.execute('''
                INSERT INTO revenue_projection (username, business_name, year, revenue, expenditure)
                VALUES (?, ?, ?, ?, ?)
            ''', (username, data["business_name"], projection["year"], projection["revenue"], projection["expenditure"]))

        print("Inserting market analysis data...")
        # Insert market share data into market_analysis table
        for analysis in data["market_analysis"]:
            cursor.execute('''
                INSERT INTO market_analysis (username, business_name, competitor, market_share)
                VALUES (?, ?, ?, ?)
            ''', (username, data["business_name"], analysis["competitor"], analysis["market_share"]))

        conn.commit()
    except sqlite3.Error as e:
        print(f"Error inserting business plan: {e}")
    finally:
        conn.close()

def update_business_plan(original_business_name, data):
    """Update an existing business plan"""
    conn = sqlite3.connect("thunder.db")
    cursor = conn.cursor()
    try:
        # Update the business plan
        cursor.execute('''
            UPDATE business_plans
            SET business_name = ?, date_created = ?, industry = ?, num_employees = ?, legal_structure = ?, percentage = ?
            WHERE business_name = ? AND username = ?
        ''', (
            data["business_name"],
            datetime.now().isoformat(),
            data["industry"],
            data["employees"],
            data["legal_structure"],
            data["percentage"],
            original_business_name,
            data["username"]
        ))

        # Update the executive summary
        cursor.execute('''
            UPDATE executive_summary
            SET description = ?, mission_statement = ?, principal_members = ?, future = ?
            WHERE business_name = ? AND username = ?
        ''', (
            data["description"],
            data["mission_statement"],
            data["principal_members"],
            data["future"],
            original_business_name,
            data["username"]
        ))

        # Update the market research
        cursor.execute('''
            UPDATE market_research
            SET industry = ?, competitors = ?, target_audience = ?, company_advantages = ?, regulations = ?
            WHERE business_name = ? AND username = ?
        ''', (
            data["industry_state"],
            data["competitors"],
            data["target_audience"],
            data["company_advantages"],
            data["regulations_compliance"],
            original_business_name,
            data["username"]
        ))

        # Update the marketing strategy
        cursor.execute('''
            UPDATE marketing_strategy
            SET growth_strategy = ?, advertising = ?, marketing_budget = ?, customer_interaction = ?, customer_retention = ?
            WHERE business_name = ? AND username = ?
        ''', (
            data["growth_strategy"],
            data["advertising_plan"],
            data["marketing_budget"],
            data["customer_interaction"],
            data["customer_retention"],
            original_business_name,
            data["username"]
        ))

        # Update the service line
        cursor.execute('''
            UPDATE service_line
            SET products = ?, services = ?, pricing_structure = ?, research_development = ?
            WHERE business_name = ? AND username = ?
        ''', (
            data["products"],
            data["services"],
            data["pricing"],
            data["research"],
            original_business_name,
            data["username"]
        ))

        # Update the contact information
        cursor.execute('''
            UPDATE contact_information
            SET contact_name = ?, address = ?, city = ?, state = ?, zip = ?, phone = ?, email = ?
            WHERE business_name = ? AND username = ?
        ''', (
            data["contact_name"],
            data["address"],
            data["city"],
            data["state"],
            data["zip_code"],
            data["phone"],
            data["email"],
            original_business_name,
            data["username"]
        ))

        # Update the financial section
        cursor.execute('''
            UPDATE financial
            SET financing_sought = ?, profit_loss_statement = ?, break_even_analysis = ?, return_on_investment = ?, contingency_plan = ?, disaster_recovery = ?, bank = ?, accounting_firm = ?, insurance_info = ?
            WHERE business_name = ? AND username = ?
        ''', (
            data["financing_sought"],
            data["profit_loss_statement"],
            data["break_even_analysis"],
            data["roi"],
            data["contingency_plan"],
            data["disaster_recovery_plan"],
            data["bank"],
            data["accounting_firm"],
            data["insurance_info"],
            original_business_name,
            data["username"]
        ))

        # Update the legal section
        cursor.execute('''
            UPDATE legal
            SET intellectual_property = ?, law_firm = ?
            WHERE business_name = ? AND username = ?
        ''', (
            data["intellectual_property"],
            data["law_firm"],
            original_business_name,
            data["username"]
        ))

        # Delete old revenue projections
        cursor.execute('''
            DELETE FROM revenue_projection
            WHERE username = ? AND business_name = ?
        ''', (data["username"], original_business_name))

        # Insert updated revenue projections
        for projection in data["revenue_projection"]:
            cursor.execute('''
                INSERT INTO revenue_projection (username, business_name, year, revenue, expenditure)
                VALUES (?, ?, ?, ?, ?)
            ''', (data["username"], data["business_name"], projection["year"], projection["revenue"], projection["expenditure"]))

        # Delete old market analysis data
        cursor.execute('''
            DELETE FROM market_analysis
            WHERE username = ? AND business_name = ?
        ''', (data["username"], original_business_name))

        # Insert updated market analysis data
        print("Inserting market analysis data...")
        for analysis in data["market_analysis"]:
            cursor.execute('''
                INSERT INTO market_analysis (username, business_name, competitor, market_share)
                VALUES (?, ?, ?, ?)
            ''', (data["username"], data["business_name"], analysis["competitor"], analysis["market_share"]))

        conn.commit()
    except sqlite3.Error as e:
        print(f"Error updating business plan: {e}")
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

#def get_business_plan_data(username, business_name):
   # """Fetch the business plan data from the database for the given username and business_name."""
   # connection = sqlite3.connect("thunder.db") 
   # cursor = connection.cursor()
    
   # query = """
   # SELECT description, mission_statement
   # FROM executive_summary
   # WHERE username = ? AND business_name = ?
   # """
   # cursor.execute(query, (username, business_name))
    
   # result = cursor.fetchone()  
    
   # connection.close()
    
   # if result:
    #    return result  
    #else:
   #     return None          
    

def get_business_plan_data(username, business_name):
    """Get all data stored in databse and return as dictionary"""
    connection = sqlite3.connect('thunder.db')
    cursor = connection.cursor()

    # Dictionary to hold business plan data
    business_plan_data = {}

    # Get data from business_plans table
    cursor.execute('''SELECT * FROM business_plans WHERE username = ? AND business_name = ?''', (username, business_name))
    business_plan_data['business_plans'] = cursor.fetchone()

    # Get data from executive_summary table
    cursor.execute('''SELECT * FROM executive_summary WHERE username = ? AND business_name = ?''', (username, business_name))
    business_plan_data['executive_summary'] = cursor.fetchone()

    # Get data from market_research table
    cursor.execute('''SELECT * FROM market_research WHERE username = ? AND business_name = ?''', (username, business_name))
    business_plan_data['market_research'] = cursor.fetchone()

    # Get data from marketing_strategy table
    cursor.execute('''SELECT * FROM marketing_strategy WHERE username = ? AND business_name = ?''', (username, business_name))
    business_plan_data['marketing_strategy'] = cursor.fetchone()

    # Get data from service_line table
    cursor.execute('''SELECT * FROM service_line WHERE username = ? AND business_name = ?''', (username, business_name))
    business_plan_data['service_line'] = cursor.fetchone()

    # Get data from contact_information table
    cursor.execute('''SELECT * FROM contact_information WHERE username = ? AND business_name = ?''', (username, business_name))
    business_plan_data['contact_information'] = cursor.fetchone()

    # Get data from financial table
    cursor.execute('''SELECT * FROM financial WHERE username = ? AND business_name = ?''', (username, business_name))
    business_plan_data['financial'] = cursor.fetchone()

    # Get data from legal table
    cursor.execute('''SELECT * FROM legal WHERE username = ? AND business_name = ?''', (username, business_name))
    business_plan_data['legal'] = cursor.fetchone()

    # Close connection
    connection.close()

    return business_plan_data

    
def get_revenue_projection(username, business_name):
    """Fetch revenue projection data for a business plan."""
    conn = sqlite3.connect("thunder.db")
    cursor = conn.cursor()
    try:
        cursor.execute('''
            SELECT year, revenue, expenditure
            FROM revenue_projection
            WHERE username = ? AND business_name = ?
            ORDER BY year
        ''', (username, business_name))
        return cursor.fetchall()  # Returns a list of tuples [(year, revenue, expenditure), ...]
    finally:
        conn.close()

def get_market_share_projection(username, business_name):
    """Fetch market analysis data for a business plan."""
    conn = sqlite3.connect("thunder.db")
    cursor = conn.cursor()
    try:
        cursor.execute('''
            SELECT competitor, market_share
            FROM market_analysis
            WHERE username = ? AND business_name = ?
            ORDER BY competitor
        ''', (username, business_name))
        return cursor.fetchall()  # Returns a list of tuples [(competitor, market_share), ...]
    finally:
        conn.close()

def resource_path(relative_path):
    """Check path to images when running packaged application"""
    # Check if running in a PyInstaller bundle
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)