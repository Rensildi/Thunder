from customtkinter import *
from newplan import BusinessPlanForm
from datetime import datetime
import sqlite3
import requests
from tkinter import messagebox
from supabase import *
from CTkMessagebox import CTkMessagebox
from PIL import Image, ImageTk
from database import resource_path
import threading

question_mark_image = Image.open(resource_path("images/help-icon.png"))
question_mark_image = question_mark_image.resize((20, 20), Image.Resampling.LANCZOS)
question_mark_ctk_image = CTkImage(light_image=question_mark_image, dark_image=question_mark_image, size=(20, 20))

def help_explanation(message, event=None):
    """Help button explanation"""
    CTkMessagebox(title="Explanation", message=message, icon="info")

class Dashboard(CTkFrame):
    def __init__(self, main_app, username):
        """Initialize dashboard"""
        super().__init__(master=main_app.root)  
        self.main_app = main_app  
        self.username = username 
        
        self.open_windows = []  # List to keep track of open business plan windows
        
        # Get supabase connection from main
        self.supabase = main_app.supabase
        self.login_timestamp = datetime.now().isoformat()

        self.page_size = 8  # Number of plans per page
        self.current_page = 1  # Track the current page number
        
        self.id, self.email = self.get_user_details()
        
        # Tutorial feature
        self.tutorial_enabled = True # Default state of Tutorial
        
        
        self.create_widgets()  
        self.load_business_plans() 

    def create_widgets(self):
        """Create widgets"""
        # Dashboard Label
        self.label = CTkLabel(
            self,
            text=f"Thunder",
            font=("Arial", 24))
        self.label.pack(pady=20)

        # # "Create New Business Plan" Button
        self.create_plan_button = CTkButton(self, text="Create New Business Plan", command=self.open_business_plan_form)
        self.create_plan_button.pack(pady=10)  
        
        # # Logout Button
        # self.logout_button = CTkButton(self, text="Logout", command=self.logout)
        # self.logout_button.pack(pady=10)
        
        # Dropdown display
        
        # Adding options
        options = [
            "Profile",
            "New plan",
            "Disable Tutorial",
            "Feedback",
            "Settings",
            "Log Out"
        ]
        self.dropdown_menu = CTkOptionMenu(self, values=options, command=self.option_selected)
        self.dropdown_menu.set(self.username) # Set initial text to username
        # Position == Top Right (NE)
        self.dropdown_menu.place(relx=1.0, x=-10, y=10, anchor="ne")

        # Search Entry
        self.search_entry = CTkEntry(self, placeholder_text="Search Business Plans...")
        self.search_entry.pack(pady=10, padx=250, fill='x')
        self.search_entry.bind("<KeyRelease>", self.update_listbox)

        # Frame to display the business plans
        self.plans_frame = CTkFrame(self)  
        self.plans_frame.pack(pady=10, padx=250, fill='both')  

        # Create a frame for the page controls and the business plans
        self.controls_frame = CTkFrame(self)
        self.controls_frame.pack(pady=10, padx=250, fill='x')

        # Page Navigation Buttons
        self.prev_button = CTkButton(self.controls_frame, text="Previous", command=lambda: self.change_page(-1))
        self.prev_button.pack(side='left', padx=15)

        self.next_button = CTkButton(self.controls_frame, text="Next", command=lambda: self.change_page(1))
        self.next_button.pack(side='right', padx=15)
        
        # Notification Label
        self.notification_label = CTkLabel(
            self, 
            text=(f"Welcome {self.username}"), 
            font=("Arial", 16), 
            fg_color="gray",
            width=300, 
            height=40
            )
        self.notification_label.place(
            relx=0.5,
            y=10,
            anchor="n" # Near to the top center is positioned
        )
        self.notification_label.pack_forget() # By default notification is hidden
        
        self.add_help_icons()
        
    def get_user_details(self):
        ''' Fetch user details'''
        conn = sqlite3.connect("thunder.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, email FROM users WHERE username = ?", (self.username,))
        user_details = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user_details:
            return user_details # Return user id and email
        else:
            print("User details not found!")
            return None, None
    
    def add_help_icons(self):
        ''' Add the help icons (with their initial positions stored) '''
        self.help_icons = []  # Store the icons and their positions
        
        # Create and place help icons with stored positions
        help_icon_label = CTkLabel(self, text="", image=question_mark_ctk_image)
        help_icon_label.place(relx=0.0065, rely=0.0065)
        self.help_icons.append({'icon': help_icon_label, 'relx': 0.0065, 'rely': 0.0065})
        help_icon_label.bind("<Button-1>", lambda e: help_explanation("This is your dashboard where you can manage your business plans."))
        
        help_icon_label = CTkLabel(self, text="", image=question_mark_ctk_image)
        help_icon_label.place(relx=0.6, rely=0.13)
        self.help_icons.append({'icon': help_icon_label, 'relx': 0.6, 'rely': 0.13})
        help_icon_label.bind("<Button-1>", lambda e: help_explanation("Click here to create a new business plan."))
        
        help_icon_label = CTkLabel(self, text="", image=question_mark_ctk_image)
        help_icon_label.place(relx=0.80, rely=0.017799)
        self.help_icons.append({'icon': help_icon_label, 'relx': 0.80, 'rely': 0.017799})
        help_icon_label.bind("<Button-1>", lambda e: help_explanation("Use this dropdown to navigate to different sections of the app."))
        
        help_icon_label = CTkLabel(self, text="", image=question_mark_ctk_image)
        help_icon_label.place(relx=0.7283, rely=0.208)
        self.help_icons.append({'icon': help_icon_label, 'relx': 0.7283, 'rely': 0.208})
        help_icon_label.bind("<Button-1>", lambda e: help_explanation("Search for your business plans here."))
        
        help_icon_label = CTkLabel(self, text="", image=question_mark_ctk_image)
        help_icon_label.place(relx=0.7283, rely=0.29)
        self.help_icons.append({'icon': help_icon_label, 'relx': 0.7283, 'rely': 0.29})
        help_icon_label.bind("<Button-1>", lambda e: help_explanation("Navigate through pages of your business plans using these buttons."))
        
        # Initially hide help icons if tutorial is disabled.
        if not self.tutorial_enabled:
            self.update_help_icons()

    
    
    ### NOTIFICATION FEATURE
    
    # def show_notification(self, message="This is a notification!", duration=3):
    #     ''' Notification toast-style '''
    #     self.notification_label.configure(text=message) # Update message
    #     self.notification_label.pack() # Show the notification
        
    #     # Hide the notification after 3 seconds
    #     self.after(duration * 1000, self.remove_notification)
    
    # def remove_notification(self):
    #     ''' Hide the notification after 3 seconds '''
    #     self.notification_label.pack_forget()
        

    def option_selected(self, selected_option):
        ''' Handle the option selected from the dropdown '''
        if selected_option == "Profile":
            self.show_profile() # Handle profile action if needed
        elif selected_option == "New plan":
            self.open_business_plan_form() # Call the functio nto create a new business plan
        elif selected_option == "Disable Tutorial":
            self.toggle_tutorial()
        elif selected_option == "Feedback":
            self.open_feedback_window()
        elif selected_option == "Settings":
            self.show_settings() # Handle settings action if needed
        elif selected_option == "Log Out":
            self.logout() # Call logout functionality
        
        # Reset the dorpdown to show the username again after selection
        self.dropdown_menu.set(self.username)
    
    def open_business_plan_form(self):
        """Open the business plan form in a new window"""
        plan_window = BusinessPlanForm(self, self.username)
        plan_window.protocol("WM_DELETE_WINDOW", lambda: self.close_business_plan_window(plan_window))  
        self.open_windows.append(plan_window)  
        
    def is_online(self):
        """Check internet connection"""
        try:
            requests.get("https://www.google.com", timeout=3)
            return True
        except requests.ConnectionError:
            return False
        
    def push_to_supabase(self):
        """Push all new and unsynced login/business plan records to Supabase."""
        conn = sqlite3.connect("thunder.db")
        cursor = conn.cursor()

        # Fetch all rows with pushed = 'N' for the user
        cursor.execute("""
            SELECT id, username, login_timestamp, logout_timestamp FROM logins
            WHERE username = ? AND pushed = 'N'
        """, (self.username,))
        rows = cursor.fetchall()

        if not rows:
            print("No records to push.")
        else:    
            # Insert into supabase
            login_data_to_insert = [
                {"username": row[1], "login": row[2], "logout": row[3]}
                for row in rows
            ]
            try:
                # Insert into supabase
                response = self.supabase.table("logins").insert(login_data_to_insert).execute()

                # Check if the request was successful and if so, update pushed markers
                if response.data:
                    print("Successfully pushed to Supabase.")
                    
                    # Update local database to mark rows as pushed
                    row_ids = [row[0] for row in rows]
                    # Create placeholders dynamically
                    placeholders = ', '.join(['?'] * len(row_ids))

                    # SQL query for updating the pushed/not pushed marker
                    update_query = """
                        UPDATE logins
                        SET pushed = 'Y'
                        WHERE id IN ({})
                    """.format(placeholders)

                    cursor.execute(update_query, row_ids)
                    conn.commit()

                elif response.error: 
                    print("Error pushing to Supabase:", response.error)
                    
            except Exception as e:
                print("Error pushing to Supabase:", e)


        # Get records from local db
        cursor.execute("""
            SELECT username, business_name, percentage FROM business_plans
            WHERE username = ?
        """, (self.username,))
        rows = cursor.fetchall()

        if not rows:
            print("No records to push.")
            conn.close()
            return

        # Prepare data for supabase
        business_data_to_insert = [
            {"p_username": row[0], "p_plan_name": row[1], "p_completion_percentage": row[2]}
            for row in rows
        ]

        # Upsert to supabase (function defined in supabase because would not recognize unique constraint via python code)
        try:
            for data in business_data_to_insert:
                response = self.supabase.rpc("upsert_plans", data).execute()

        except Exception as e:
            print("Error pushing to Supabase:", e)

        finally:
            conn.close()

    def logout(self):
        """Logout of application and update supabase"""
        if self.open_windows:  
            messagebox.showwarning("Warning", "Please close all open Business Plan windows before logging out.")
        else:
            logout_timestamp = datetime.now().isoformat()
            print(f"User {self.username} logged out at {logout_timestamp}")

            # Update local db
            conn = sqlite3.connect("thunder.db")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO logins (username, login_timestamp, logout_timestamp, pushed)
                VALUES (?, ?, ?, 'N')
            """, (self.username, self.login_timestamp, logout_timestamp))
            conn.commit()
            conn.close()

            # Push to supabase if app connected to internet
            if self.is_online():
                self.push_to_supabase()

            self.pack_forget()
            self.main_app.show_signin()
    
    def show_profile(self):
        '''Navigating to the user profile'''
        print(f"Showing profile for {self.username}")
        # The profile view is not yet implemented
    
    def toggle_tutorial(self):
        ''' Toggle the visibility of the tutorial help-icons (the question marks)'''
        
        if not hasattr(self, 'help_icons'):
            self.add_help_icons()
            
        self.tutorial_enabled = not self.tutorial_enabled
        print(f"Tutorial enabled: {self.tutorial_enabled}")
        
        self.update_help_icons()
        
        # Update dropdown Tutorial label
        if self.tutorial_enabled:
            self.dropdown_menu.set("Disable Tutorial")
        else:
            self.dropdown_menu.set("Enable Tutorial")
    
    def update_help_icons(self):
        ''' Update the visibility of the help icons based on tutorial state.'''
        
        if self.tutorial_enabled:
            for icon_info in self.help_icons:
                icon_info['icon'].place(
                    relx=icon_info['relx'], 
                    rely=icon_info['rely']
                    )
                # help_icon = icon_info['icon']
                # relx = icon_info['relx']
                # rely = icon_info['rely']
                # help_icon.place(relx=relx, rely=rely)
            print("Help icons visible: True")
        else:
            for icon_info in self.help_icons:
                icon_info['icon'].place_forget() # Hide the icons
        print("Help icons visible: False")
    
    def open_feedback_window(self):
        '''Open the feedback window.'''
        from feedback import FeedbackForm
        feedback_window = FeedbackForm(self, self.id, self.email, self.username)
        feedback_window.mainloop()
    
    def show_settings(self):
        '''Navigate to the settings page'''
        print(f"Openining Settings...")
        # The settings view is not yet implemented

    def load_business_plans(self):
        """Load previous business plans for the logged-in user and paginate"""
        self.update_page_buttons()  

        # Clear previous business plans
        for widget in self.plans_frame.winfo_children():
            widget.destroy()

        conn = sqlite3.connect("thunder.db")
        cursor = conn.cursor()

        # Limit the results based on current page
        offset = (self.current_page - 1) * self.page_size
        cursor.execute("SELECT business_name, date_created FROM business_plans WHERE username=? LIMIT ? OFFSET ?", 
                       (self.username, self.page_size, offset))
        plans = cursor.fetchall()

        if not plans:  
            # Display a message if no plans are available
            no_plans_label = CTkLabel(self.plans_frame, text="No saved plans available. Start planning today!", font=("Arial", 14), text_color="gray")
            no_plans_label.pack(pady=20)
        else:
            # Create buttons for each business plan
            for plan in plans:
                business_name = plan[0]
                date = plan[1]
                date_obj = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f")
                formatted_date = date_obj.strftime("%m-%d-%Y")
                button_text = f"{business_name} - {formatted_date}"
                button = CTkButton(self.plans_frame, text=button_text, border_width=0, command=lambda name=business_name: self.edit_selected_plan(name))
                button.pack(pady=5, padx=15, fill='x') 
            
        cursor.close()
        conn.close()

    def update_listbox(self, event=None):
        """Update the list of business plans after user search"""
        search_term = self.search_entry.get().lower()
        
        # Clear previous business plans
        for widget in self.plans_frame.winfo_children():
            widget.destroy()

        conn = sqlite3.connect("thunder.db")
        cursor = conn.cursor()

        # Search term
        offset = (self.current_page - 1) * self.page_size
        cursor.execute("SELECT business_name, date_created FROM business_plans WHERE username=? AND business_name LIKE ? LIMIT ? OFFSET ?", 
                       (self.username, f"%{search_term}%", self.page_size, offset))
        plans = cursor.fetchall()

        # Create buttons for each matching business plan
        for plan in plans:
                business_name = plan[0]
                date = plan[1]
                date_obj = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f")
                formatted_date = date_obj.strftime("%m-%d-%Y")
                button_text = f"{business_name} - {formatted_date}"
                button = CTkButton(self.plans_frame, text=button_text, border_width=0, command=lambda name=business_name: self.edit_selected_plan(name))
                button.pack(pady=5, padx=15, fill='x') 
        
        cursor.close()
        conn.close()

    def change_page(self, direction):
        """Change the current page (next/previous)"""
        new_page = self.current_page + direction
        # Ensure the page stays within bounds
        if new_page > 0:
            self.current_page = new_page
            self.load_business_plans()

    def update_page_buttons(self):
        """Disable the Previous/Next buttons if on the first/last page"""
        conn = sqlite3.connect("thunder.db")
        cursor = conn.cursor()

        # Count the total number of business plans for the user
        cursor.execute("SELECT COUNT(*) FROM business_plans WHERE username=?", (self.username,))
        total_plans = cursor.fetchone()[0]
        total_pages = (total_plans + self.page_size - 1) // self.page_size  # Calculate total pages

        # Disable "Previous" button if on the first page
        if self.current_page == 1:
            self.prev_button.configure(state='disabled')
        else:
            self.prev_button.configure(state='normal')

        # Disable "Next" button if on the last page
        if self.current_page == total_pages:
            self.next_button.configure(state='disabled')
        else:
            self.next_button.configure(state='normal')

        cursor.close()
        conn.close()

    def connect_db(self):
        """Connect to DB"""
        return sqlite3.connect('thunder.db') 

    def edit_selected_plan(self, business_name):
        """Open the edit window for the selected business plan"""
        business_plan_details = self.fetch_business_plan_details(business_name)
        
        if business_plan_details:
            description, mission_statement = business_plan_details
            plan_window = BusinessPlanForm(self, self.username, business_name, description, mission_statement)
            plan_window.protocol("WM_DELETE_WINDOW", lambda: self.close_business_plan_window(plan_window))  
            self.open_windows.append(plan_window)  
        else:
            print("Business plan not found.")

    def fetch_business_plan_details(self, business_name):
        """Retrieve business plan details from the database"""
        try:
            conn = self.connect_db()  
            cursor = conn.cursor()

            cursor.execute("""SELECT description, mission_statement FROM executive_summary WHERE business_name = ?""", (business_name,))
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
            self.open_windows.remove(window)  
        window.destroy()  

if __name__ == "__main__":
    pass