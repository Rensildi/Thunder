from customtkinter import *
from newplan import BusinessPlanForm
from datetime import datetime
import sqlite3
from tkinter import messagebox

class Dashboard(CTkFrame):
    def __init__(self, main_app, username):
        super().__init__(master=main_app.root)  # Set the main app's root as the master
        self.main_app = main_app  # Store reference to the main app
        self.username = username  # Store the username
        self.open_windows = []  # List to keep track of open business plan windows
        
        self.create_widgets()  # Call method to create widgets
        self.load_business_plans()  # Load existing business plans

    def create_widgets(self):
        # Dashboard Label
        self.label = CTkLabel(self, text=f"Welcome to the Dashboard, {self.username}!", font=("Arial", 24))
        self.label.pack(pady=20)

        # "Create New Business Plan" Button
        self.create_plan_button = CTkButton(self, text="Create New Business Plan", command=self.open_business_plan_form)
        self.create_plan_button.pack(pady=10)
        
        # Logout Button
        self.logout_button = CTkButton(self, text="Logout", command=self.logout)
        self.logout_button.pack(pady=10)

        # Search Entry
        self.search_entry = CTkEntry(self, placeholder_text="Search Business Plans...")
        self.search_entry.pack(pady=10, padx=250, fill='x')
        self.search_entry.bind("<KeyRelease>", self.update_listbox)

        # Create a frame for the scrollable area
        self.plans_frame = CTkFrame(self, bg_color="#d3d3d3")  
        self.plans_frame.pack(pady=10, padx=250, fill='x')  

        # Create a canvas to hold the buttons
        self.canvas = CTkCanvas(self.plans_frame, bg="#3A3A3A", highlightthickness=0)
        self.scrollbar = CTkScrollbar(self.plans_frame, command=self.canvas.yview)

        self.scrollable_frame = CTkFrame(self.canvas, bg_color="#3A3A3A")
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Create a window in the canvas to hold the scrollable frame
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Pack the scrollbar and canvas
        self.scrollbar.pack(side='right', fill='y')
        self.canvas.pack(side='left', fill='both', expand=True)

        # Configure canvas scrolling
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
    
    def open_business_plan_form(self):
        # Open the business plan form in a new window
        plan_window = BusinessPlanForm(self, self.username)
        plan_window.protocol("WM_DELETE_WINDOW", lambda: self.close_business_plan_window(plan_window))  # Handle close event
        self.open_windows.append(plan_window)  # Keep track of the open window
        
    def logout(self):
        if self.open_windows:  # Check if there are any open business plan windows
            messagebox.showwarning("Warning", "Please close all open Business Plan windows before logging out.")
        else:
            self.pack_forget()
            self.main_app.show_signin()

    def load_business_plans(self):
        """Load previous business plans for the logged in user"""
        # Clear previous buttons
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        conn = sqlite3.connect("thunder.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT business_name, date_created FROM business_plans WHERE username=?", (self.username,))
        plans = cursor.fetchall()
        
        # Create buttons for each business plan
        for plan in plans:
            business_name = plan[0]
            date = plan[1]
            date_obj = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f")
            formatted_date = date_obj.strftime("%m-%d-%Y")
            button_text = f"{business_name} - {formatted_date}"
            button = CTkButton(self.scrollable_frame, text=button_text, border_width=0, command=lambda name=business_name: self.edit_selected_plan(name))
            button.pack(pady=5, fill='x', expand=True)  
        
        cursor.close()
        conn.close()

    def update_listbox(self, event=None):
        """Update the list of business plans after user search"""
        search_term = self.search_entry.get().lower()
        
        # Clear previous buttons
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        conn = sqlite3.connect("thunder.db")
        cursor = conn.cursor()

        cursor.execute("SELECT business_name FROM business_plans WHERE username=? AND business_name LIKE ?", 
                       (self.username, f"%{search_term}%"))
        plans = cursor.fetchall()

        # Create buttons for each matching business plan
        for plan in plans:
            business_name = plan[0]
            button = CTkButton(self.scrollable_frame, text=business_name, border_width=0, command=lambda name=business_name: self.edit_selected_plan(name))
            button.pack(pady=5, fill='x', expand=True)
        
        cursor.close()
        conn.close()

    def connect_db(self):
        return sqlite3.connect('thunder.db') 

    def edit_selected_plan(self, business_name):
        """Open the edit window for the selected business plan"""
        business_plan_details = self.fetch_business_plan_details(business_name)
        
        if business_plan_details:
            description, goals, target_audience = business_plan_details
            plan_window = BusinessPlanForm(self, self.username, business_name, description, goals, target_audience)
            plan_window.protocol("WM_DELETE_WINDOW", lambda: self.close_business_plan_window(plan_window))  # Handle close event
            self.open_windows.append(plan_window)  # Keep track of the open window
        else:
            print("Business plan not found.")

    def fetch_business_plan_details(self, business_name):
        """Retrieve business plan details from the database"""
        try:
            conn = self.connect_db()  
            cursor = conn.cursor()

            cursor.execute("""
                SELECT description, goals, target_audience 
                FROM business_plans 
                WHERE business_name = ?
            """, (business_name,))

            result = cursor.fetchone()

            if result:
                return result  
            else:
                print("No business plan found with that name.")
                return None

        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            if conn:  
                conn.close()

    def close_business_plan_window(self, window):
        """Remove the window from the list of open windows and destroy it."""
        if window in self.open_windows:
            self.open_windows.remove(window)  # Remove the window from the list
        window.destroy()  # Destroy the window

if __name__ == "__main__":
    pass  # The main application will handle the instantiation
