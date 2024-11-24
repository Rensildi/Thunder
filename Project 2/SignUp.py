from customtkinter import *
from PIL import Image, ImageDraw, ImageOps
from email_validator import validate_email, EmailNotValidError
import sqlite3
import bcrypt 
import database
import re
import google.auth
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dotenv import load_dotenv
from database import resource_path
import os


class SignUp(CTkFrame):
    def __init__(self, main_app):
        """Initialize sign up class"""
        super().__init__(main_app.root)  # Pass the main app's root
        self.main_app = main_app
        self.create_widgets()

    def create_widgets(self):
        self.widget_welcome_section()
        self.widget_email_section()
        self.widget_username_section()
        self.widget_password_section()
        self.widget_sign_up_button()
        self.widget_alternative_sign_up_button()
        self.widget_return_to_sign_in_button()  
        self.widget_image_section()

    def widget_image_section(self):
        """Add an image to the left side of the window"""
        image_path = resource_path("images/signup.jpg")
        pil_image = Image.open(image_path).convert("RGBA")  # Ensure image has alpha channel for transparency

        # Set radius for rounded corners
        radius = 20 

        # Create mask
        rounded_mask = Image.new("L", pil_image.size, 0)
        draw = ImageDraw.Draw(rounded_mask)
        draw.rounded_rectangle((0, 0) + pil_image.size, radius=radius, fill=255)

        # Apply mask
        rounded_image = ImageOps.fit(pil_image, pil_image.size)
        rounded_image.putalpha(rounded_mask)  

        image = CTkImage(light_image=rounded_image, size=(350, 475))  

        self.image_label = CTkLabel(master=self, image=image, text="")  
        self.image_label.place(relx=0.26, rely=0.52, anchor="center")   

    
    def widget_welcome_section(self):
        """Welcome widget"""
        # Welcome Label
        self.welcome_label = CTkLabel(master=self, text="Welcome to Thunder", font=("Arial", 30))
        self.welcome_label.place(relx=0.7, rely=0.089, anchor="center")

        # Description label
        self.description_label = CTkLabel(master=self, text="This is a description", font=("Arial", 14), text_color="grey")
        self.description_label.place(relx=0.7, rely=0.145, anchor="center")
    
    def widget_email_section(self):
        """Create email section"""
        # Email label
        self.email_label = CTkLabel(master=self, text="Email")
        self.email_label.place(relx=0.536, rely=0.16)
        
        # Asterisk for email
        self.email_asterisk = CTkLabel(master=self, text='*', text_color="red")
        self.email_asterisk.place(relx=0.58, rely=0.16)
        
        # Email entry
        self.email_entry = CTkEntry(master=self, placeholder_text="Email", width=300)
        self.email_entry.place(relx=0.7, rely=0.22, anchor="center")
        
        # Email requirements
        self.email_requirements = CTkLabel(
            master=self,
            text="Enter a valid email address.",
            text_color="grey"
        )
        self.email_requirements.place(relx=0.536, rely=0.25)

    def widget_username_section(self):
        """Create username section"""
        # Username label
        self.username_label = CTkLabel(master=self, text='Username')
        self.username_label.place(relx=0.536, rely=0.30)

        # Asterisk for username
        self.username_asterisk = CTkLabel(master=self, text='*', text_color="red")
        self.username_asterisk.place(relx=0.61, rely=0.30)

        # Username entry
        self.username_entry = CTkEntry(master=self, placeholder_text="Username", width=300)
        self.username_entry.place(relx=0.7, rely=0.36, anchor="center")

        # Username requirements
        self.username_requirements = CTkLabel(
            master=self,
            text="Choose a unique username.",
            text_color="grey"
        )
        self.username_requirements.place(relx=0.536, rely=0.383)

    def widget_password_section(self):
        """Create password section"""
        # Password label
        self.password_label = CTkLabel(master=self, text="Password")
        self.password_label.place(relx=0.536, rely=0.44)

        # Asterisk for password
        self.password_asterisk = CTkLabel(master=self, text='*', text_color="red")
        self.password_asterisk.place(relx=0.605, rely=0.44)

        # Password entry
        self.password_entry = CTkEntry(master=self, placeholder_text="Password", show="*", width=300)
        self.password_entry.place(relx=0.7, rely=0.50, anchor="center")

        # Password requirements
        self.password_requirements = CTkLabel(
            master=self,
            text="Choose a strong and unique password.",
            justify='left',
            text_color="grey",
            width=300
        )
        self.password_requirements.place(relx=0.497, rely=0.549, anchor='w')

        # Confirm Password Label
        self.confirm_password_label = CTkLabel(master=self, text="Confirm Password")
        self.confirm_password_label.place(relx=0.536, rely=0.59)

        # Asterisk for confirm password
        self.confirm_password_asterisk = CTkLabel(master=self, text='*', text_color="red")
        self.confirm_password_asterisk.place(relx=0.665, rely=0.59)

        # Confirm Password entry
        self.confirm_password_entry = CTkEntry(master=self, placeholder_text="Confirm Password", show="*", width=300)
        self.confirm_password_entry.place(relx=0.7, rely=0.65, anchor="center")

        # Confirm Password requirements
        self.confirm_password_requirements = CTkLabel(
            master=self,
            text="Enter the same Password as before",
            text_color="grey"
        )
        self.confirm_password_requirements.place(relx=0.536, rely=0.699, anchor="w")

    def widget_sign_up_button(self):
        """Create sign up section"""
        # Sign Up button
        self.sign_up_button = CTkButton(master=self, text="Sign Up", width=300, height=30, command=self.sign_up)
        self.sign_up_button.place(relx=0.7, rely=0.755, anchor="center")

    def widget_alternative_sign_up_button(self):
        """Alternative sign up Google button"""
        self.continue_google_button = CTkButton(master=self, text="Continue With Google", width=300, height=30, command=self.sign_up_with_google)
        self.continue_google_button.place(relx=0.7, rely=0.823, anchor="center")
    
    def sign_up_with_google(self):
        """ Initiates Google OAuth flow using environment variables. """
        SCOPES = ['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email']

        # Retrieve the path to the client secrets file from environment variables or a fixed location
        google_client_secrets_file = resource_path('client_secrets.json')

        if not os.path.exists(google_client_secrets_file):
            print("Google client secrets file not found.")
            return

        try:
            # Initialize the OAuth flow using the client secrets file
            flow = InstalledAppFlow.from_client_secrets_file(google_client_secrets_file, SCOPES)
            credentials = flow.run_local_server(port=8080)

            # Use the credentials to build the service
            service = build('people', 'v1', credentials=credentials)
            profile = service.people().get(resourceName='people/me', personFields='names,emailAddresses').execute()

            email = profile['emailAddresses'][0]['value']
            username = profile['names'][0]['displayName']

            self.process_google_signup(email, username)
        except ValueError as e:
            print(f"Error with client secrets format: {e}")
        except Exception as e:
            print(f"Error occurred while fetching Google user info: {e}")


            
    def process_google_signup(self, email, username):
        """ Handles Google sign-up and user creation """
        # Check if email already exists
        conn = sqlite3.connect('thunder.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()

        if user:
            # User already exists, proceed to login
            self.update_console(f"User with email {email} already exists. Logging in...")
            self.sign_in_with_google(email)
        else:
            # New user, proceed with sign-up
            self.create_new_user(email, username)

        conn.close()
    
    def create_new_user(self, email, username):
        """Creates a new user in the database with Google credentials"""
        
        # Insert the new user into the database (no need for password)
        conn = sqlite3.connect('thunder.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (email, username) VALUES (?, ?)", (email, username))
        conn.commit()
        conn.close()

        self.update_console("Account created successfully! Logging you in now...")
        #self.sign_in_with_google(email)
    
    def sign_in_with_google(self, email):
        """ "Handle user login with Google credentials" """
        
        # Proceed with sign-in
        self.update_console(f"Signing in with Google account: {email}")
    
    def update_console(self, message):
        """Update console output"""
        self.console_output.configure(text=message)
        

    def widget_return_to_sign_in_button(self):
        """Return to sign in screen button"""
        self.return_button = CTkButton(master=self, text="Back to Sign In", width=300, height=30, command=self.return_to_sign_in)
        self.return_button.place(relx=0.7, rely=0.891, anchor="center")  # Adjust position as needed
    

    def reset_form(self):
        """Clear all input fields and reset error messages"""
        self.username_entry.delete(0, "end")
        self.password_entry.delete(0, "end")
        self.confirm_password_entry.delete(0, "end")
        
        # Hide error label if it exists
        if hasattr(self, "error_label"):
            self.error_label.configure(text="")
        
        # Hide successfully created account message if it exists
        if hasattr(self, "account_created_message"):
            self.account_created_message.place_forget()
    
    def return_to_sign_in(self):
        """Return to the sign-in screen and reset the form"""
        self.reset_form()
        self.main_app.show_signin()  # Call the main app's method to show the SignIn screen

    def sign_up(self):
        """Main sign up function"""
        email = self.email_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        # Error handling labels
        def error_message(label, message):
            label.configure(text=message)
            label.place(relx=0.7, rely=0.95, anchor="center")
        
        # Validate inputs
        if not hasattr(self, 'error_label'):
            self.error_label = CTkLabel(master=self, text="", text_color = "red")
            
        # Validation of email with email-validator library
        try:
            validate_email(email)
        except EmailNotValidError as e:
            error_message(self.error_label, f"Invalid email: {str(e)}")
            return
            
        # Previous version of email validation
        # if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
        #     error_message(self.error_label, "Invalid email address!")
        #     return
            
        if not re.match("^[A-Za-z0-9@.+-_]{1,150}$", username):
            self.error_label.configure(text="Not all Username requirements are met!")
            self.error_label.place(relx=0.7, rely=0.95, anchor="center")
            return
        
        if not email or not username or not password or not confirm_password:
            error_message(self.error_label, " All fields are required!")
            return
        
        if password != confirm_password:
            error_message(self.error_label, "Passwords do not match!")
            return
        
        if len(password) < 8:
            error_message(self.error_label, "Password must be at least 8 characters long!")
            return
        
        else:
            self.error_label.place_forget()
        
        conn = sqlite3.connect('thunder.db')
        cursor = conn.cursor()
        
        # Check if the email already exists
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            error_message(self.error_label, "Email already exists!")
            cursor.close()
            conn.close()
            return
        
        # Check if the username already exists
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        if cursor.fetchone(): # When result is found, username exits
            error_message(self.error_label, "Username already exists. Please choose another one.")
            cursor.close()
            conn.close()
            return
        
        
        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Convert hashed password to string
        hashed_password_str = hashed_password.decode('utf-8')  # Convert bytes to string

        # Insert the new user to database
        cursor.execute(
            "INSERT INTO users (email, username, password) VALUES (?, ?, ?)",
            (email, username, hashed_password_str)
        )
        
        conn.commit()    
        cursor.close()
        conn.close()
        
        # Account successfully created message
        self.account_created_message = CTkLabel(
            master=self,
            text="Account created successfully.",
            text_color="green"
        )
        self.account_created_message.place(relx=0.7, rely=0.95, anchor="center")
        
        self.after(2000, self.return_to_sign_in)
        
    def return_to_sign_in(self):
        """Return to sign in function"""
        self.reset_form()
        self.main_app.show_signin()

    def on_show(self):
        """Obscure password fields"""
        self.reset_form()
        self.password_entry.configure(show="*") # Ensure password is hidden
        self.confirm_password_entry.configure(show="*") # Ensure the confirm password is hidden

    def hide(self):
        """Hide the current section"""
        self.pack_forget() 
        
if __name__ == "__main__":
    pass
