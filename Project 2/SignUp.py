from customtkinter import *
from PIL import Image, ImageDraw, ImageOps
import sqlite3
import bcrypt 
import database
import re


class SignUp(CTkFrame):
    def __init__(self, main_app):
        super().__init__(main_app.root)  # Pass the main app's root
        self.main_app = main_app
        self.create_widgets()

    def create_widgets(self):
        self.widget_welcome_section()
        self.widget_username_section()
        self.widget_password_section()
        self.widget_sign_up_button()
        self.widget_alternative_sign_up_button()
        self.widget_return_to_sign_in_button()  
        self.widget_image_section()

    def widget_image_section(self):
        """Add an image to the left side of the window"""

        image_path = "images/signup.jpg"  
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
        self.image_label.place(relx=0.26, rely=0.51, anchor="center")   

    
    def widget_welcome_section(self):
        # Welcome Label
        self.welcome_label = CTkLabel(master=self, text="Welcome to Thunder", font=("Arial", 30))
        self.welcome_label.place(relx=0.7, rely=0.1, anchor="center")

        # Description label
        self.description_label = CTkLabel(master=self, text="This is a description", font=("Arial", 14), text_color="grey")
        self.description_label.place(relx=0.7, rely=0.15, anchor="center")

    def widget_username_section(self):
        # Username label
        self.username_label = CTkLabel(master=self, text='Username')
        self.username_label.place(relx=0.536, rely=0.22)

        # Asterisk for username
        self.username_asterisk = CTkLabel(master=self, text='*', text_color="red")
        self.username_asterisk.place(relx=0.61, rely=0.22)

        # Username entry
        self.username_entry = CTkEntry(master=self, placeholder_text="Username", width=300)
        self.username_entry.place(relx=0.7, rely=0.28, anchor="center")

        # Username requirements
        self.username_requirements = CTkLabel(
            master=self,
            text="Choose a unique username.",
            text_color="grey"
        )
        self.username_requirements.place(relx=0.536, rely=0.303)

    def widget_password_section(self):
        # Password label
        self.password_label = CTkLabel(master=self, text="Password")
        self.password_label.place(relx=0.536, rely=0.38)

        # Asterisk for password
        self.password_asterisk = CTkLabel(master=self, text='*', text_color="red")
        self.password_asterisk.place(relx=0.605, rely=0.38)

        # Password entry
        self.password_entry = CTkEntry(master=self, placeholder_text="Password", show="*", width=300)
        self.password_entry.place(relx=0.7, rely=0.44, anchor="center")

        # Password requirements
        self.password_requirements = CTkLabel(
            master=self,
            text="Choose a strong and unique password.",
            justify='left',
            text_color="grey",
            width=300
        )
        self.password_requirements.place(relx=0.497, rely=0.489, anchor='w')

        # Confirm Password Label
        self.confirm_password_label = CTkLabel(master=self, text="Confirm Password")
        self.confirm_password_label.place(relx=0.536, rely=0.54)

        # Asterisk for confirm password
        self.confirm_password_asterisk = CTkLabel(master=self, text='*', text_color="red")
        self.confirm_password_asterisk.place(relx=0.665, rely=0.54)

        # Confirm Password entry
        self.confirm_password_entry = CTkEntry(master=self, placeholder_text="Confirm Password", show="*", width=300)
        self.confirm_password_entry.place(relx=0.7, rely=0.60, anchor="center")

        # Confirm Password requirements
        self.confirm_password_requirements = CTkLabel(
            master=self,
            text="Enter the same Password as before",
            text_color="grey"
        )
        self.confirm_password_requirements.place(relx=0.536, rely=0.649, anchor="w")

    def widget_sign_up_button(self):
        # Sign Up button
        self.sign_up_button = CTkButton(master=self, text="Sign Up", width=300, height=30, command=self.sign_up)
        self.sign_up_button.place(relx=0.7, rely=0.745, anchor="center")

    def widget_alternative_sign_up_button(self):
        # Alternative sign up Google button
        self.continue_google_button = CTkButton(master=self, text="Continue With Google", width=300, height=30)
        self.continue_google_button.place(relx=0.7, rely=0.813, anchor="center")

    def widget_return_to_sign_in_button(self):
        self.return_button = CTkButton(master=self, text="Back to Sign In", width=300, height=30, command=self.return_to_sign_in)
        self.return_button.place(relx=0.7, rely=0.881, anchor="center")  # Adjust position as needed
    

    def reset_form(self):
        # Clear all input fields and reset error messages
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
        # Return to the sign-in screen and reset the form
        self.reset_form()
        self.main_app.show_signin()  # Call the main app's method to show the SignIn screen

    def sign_up(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        # Error handling labels
        def error_message(label, message):
            label.configure(text=message)
            label.place(relx=0.7, rely=0.7526, anchor="center")
        
        # Validate inputs
        if not hasattr(self, 'error_label'):
            self.error_label = CTkLabel(master=self, text="", text_color = "red")
            
        if not re.match("^[A-Za-z0-9@.+-_]{1,150}$", username):
            self.error_label.configure(text="Not all Username requirements are met!")
            self.error_label.place(relx=0.7, rely=0.7526, anchor="center")
            return
        
        if not username or not password or not confirm_password:
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
            
        # Check if the username already exists
        conn = sqlite3.connect('thunder.db')
        cursor = conn.cursor()
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

        # Call the create_user function to insert into the database
        database.create_user(username, hashed_password_str)  # Pass the string
        
        cursor.close()
        conn.close()
        
        # Account successfully created message
        self.account_created_message = CTkLabel(
            master=self,
            text="Account created successfully.",
            text_color="green"
        )
        self.account_created_message.place(relx=0.7, rely=0.7526, anchor="center")
        
        self.after(2000, self.return_to_sign_in)
        
    def return_to_sign_in(self):
        self.reset_form()
        self.main_app.show_signin()

    def on_show(self):
        self.reset_form()
        self.password_entry.configure(show="*") # Ensure password is hidden
        self.confirm_password_entry.configure(show="*") # Ensure the confirm password is hidden
    
    


    def hide(self):
        self.pack_forget()  # Use pack_forget to hide the current screen
        
if __name__ == "__main__":
    pass
