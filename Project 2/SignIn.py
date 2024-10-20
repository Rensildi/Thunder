from customtkinter import *
import createuser
import sqlite3
import bcrypt
import subprocess
from dashboard import Dashboard

class SignIn(CTkFrame):
    def __init__(self, main_app):
        super().__init__(main_app.root)  # Pass the main app's root
        self.main_app = main_app
        self.create_widgets()

    def create_widgets(self):
        self.widget_welcome_section()
        self.widget_username_section()
        self.widget_password_section()
        self.widget_sign_in_button()
        self.widget_sign_up_button()
        self.widget_console_output()
        self.widget_alternative_sign_in_button()

    def widget_welcome_section(self):
        # Welcome Label
        welcome_label = CTkLabel(master=self, text="Welcome Back", font=("Arial", 30))
        welcome_label.place(relx=0.7, rely=0.1, anchor="center")

        # Description Label
        description_label = CTkLabel(master=self, text="This is a description", font=("Arial", 14), text_color="grey")
        description_label.place(relx=0.7, rely=0.15, anchor="center")

    def widget_username_section(self):
        # Username label
        self.username_label = CTkLabel(master=self, text='Username')
        self.username_label.place(relx=0.536, rely=0.22)

        # Username entry
        self.username_entry = CTkEntry(master=self, placeholder_text="Username", width=300)
        self.username_entry.place(relx=0.7, rely=0.28, anchor="center")
        
    def widget_password_section(self):
        # Password label
        self.password_label = CTkLabel(master=self, text="Password")
        self.password_label.place(relx=0.536, rely=0.38)
        
        # Password entry
        self.password_entry = CTkEntry(master=self, placeholder_text="Password", show="*", width=300)
        self.password_entry.place(relx=0.7, rely=0.44, anchor="center")
        
        
    def widget_sign_in_button(self):
        # Sign In button
        sign_in = CTkButton(master=self, text="Sign In", command=self.sign_in)
        sign_in.configure(width=300, height=30)
        sign_in.place(relx=0.7, rely=0.6, anchor="center")

    def widget_sign_up_button(self):
        # Sign Up button
        sign_up = CTkButton(master=self, text="Sign Up", command=self.launch_signup)
        sign_up.configure(width=300, height=30)
        sign_up.place(relx=0.7, rely=0.7, anchor="center")

    def widget_alternative_sign_in_button(self):
        # Continue with Google button
        continue_google = CTkButton(master=self, text="Continue With Google")
        continue_google.configure(width=300, height=30)
        continue_google.place(relx=0.7, rely=0.8, anchor="center")

    def widget_console_output(self):
        # Create a console output area
        self.console_output = CTkLabel(master=self, text="", font=("Arial", 12), text_color="red", justify="left", wraplength=400)
        self.console_output.place(relx=0.7, rely=0.9, anchor="center")
    
    def update_console(self, message):
        # Method to update console output
        self.console_output.configure(text=message)
    
    def launch_signup(self):
        self.main_app.show_signup()  # Call the main app's method to show the SignUp screen

    def sign_in(self):
        # Implement sign-in functionality here
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # Connect to the database
        conn = sqlite3.connect('thunder.db')
        cursor = conn.cursor()
        
        # Fetch user data
        sql = "SELECT password FROM users WHERE username = ?"
        cursor.execute(sql, (username,))
        result = cursor.fetchone()
        
        # Check if username exists and password matches
        if result:
            hashed_password = result[0]  # Already a string now
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):  # Convert string to bytes for comparison
                # Open the dashboard and pass the username
                self.hide()  # Hide current frame
                dashboard = Dashboard(self.main_app, username)  # Pass the main app and username
                dashboard.pack(fill='both', expand=True)  # Pack the dashboard frame
            else:
                self.update_console("Incorrect password.")
        else:
            self.update_console("Username may not exist.")
        
        cursor.close()
        conn.close()
        print("Sign In button clicked")  # Placeholder for actual sign-in logic

    def hide(self):
        self.pack_forget()  # Use pack_forget to hide the current screen

if __name__ == "__main__":
    pass
