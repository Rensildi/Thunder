from customtkinter import *
from PIL import Image, ImageDraw, ImageOps
#import createuser
import sqlite3
import bcrypt
import subprocess
from dashboard import Dashboard
import threading

class SignIn(CTkFrame):
    def __init__(self, main_app):
        super().__init__(main_app.root)  # Pass the main app's root
        self.main_app = main_app
        self.create_widgets()
        self.angle = 0 # For rotating circle
        self.is_loading = False 

    def create_widgets(self):
        self.widget_welcome_section()
        self.widget_username_section()
        # self.widget_username_section() replaced widget_username_section() with widget_username_section()
        self.widget_password_section()
        self.widget_sign_in_button()
        self.widget_sign_up_button()
        self.widget_console_output()
        self.widget_alternative_sign_in_button()
        self.widget_image_section()
        
        # Bind Enter key to sign in function for username and password fields
        self.username_entry.bind("<Return>", self.on_enter_key_pressed)
        self.password_entry.bind("<Return>", self.on_enter_key_pressed)

        # Create a Canvas for the circular loading animation
        self.canvas = CTkCanvas(self, width=30, height=30, bg="#2E2E2E", highlightthickness=0, bd=0)
        self.canvas.place(relx=0.7, rely=0.94, anchor="center")

    def widget_image_section(self):
        """Add an image to the left side of the window"""

        image_path = "images/thunder1.jpg"  
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
        welcome_label = CTkLabel(master=self, text="Welcome Back", font=("Arial", 30))
        welcome_label.place(relx=0.7, rely=0.1, anchor="center")

        # Description Label
        description_label = CTkLabel(master=self, text="This is a description", font=("Arial", 14), text_color="grey")
        description_label.place(relx=0.7, rely=0.15, anchor="center")

    def widget_username_section(self):
        # Username label
        self.username_label = CTkLabel(master=self, text="Username")
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
        self.reset_form()
        self.main_app.show_signup()  # Call the main app's method to show the SignUp screen

    def sign_in(self):
        """Sign the user into the application by checking for valid credentials"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            self.update_console("Username and Password cannot be empty.")
            return
        
        # Start the loading animation in a separate thread
        self.is_loading = True
        self.angle = 0
        self.update_circle()
        
        # Connect to the database
        conn = sqlite3.connect('thunder.db')
        cursor = conn.cursor()
        
        try:
            # Fetch user data
            sql = "SELECT username, password FROM users WHERE username = ?"
            cursor.execute(sql, (username,))
            result = cursor.fetchone()
            
            # Check if username exists and password matches
            if result:
                username, hashed_password = result  # Already a string now
                if hashed_password and hashed_password.startswith("$2b$"):
                    if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):  # Convert string to bytes for comparison
                        self.update_console("")  # Clear any previous error messages
                        self.console_output.configure(text_color="green")  # Set text color to green for success message
                        self.update_console("You signed in successfully! Please wait a moment")
                        self.after(1000, self.show_dashboard, username)
                    else:
                        self.update_console("Username or Password may be incorrect or they do not exist.")
                        self.is_loading = False # Preventing loading animation if the sign in is incorrect
                        self.canvas.delete("all") # Clear the loading animation
                else:
                    self.update_console("Password hash in the database is invalid")
            else:
                self.update_console("Username or Password may be incorrect or they do not exist.")
                self.is_loading = False # Preventing loading animation if the sign in is incorrect
                self.canvas.delete("all") # Clear the loading animation
        except Exception as e:
            self.update_console(f"An error occurred: {e}")
        finally:
            cursor.close()
            conn.close()
        print("Sign In button clicked")  # Placeholder for actual sign-in logic

    def on_enter_key_pressed(self, event):
        """Trigger the sign in method when Enter key is pressed"""
        self.sign_in()

    def update_circle(self):
        # Check if loading should continue
        if self.is_loading:
            
            self.canvas.delete("all")
        
            x_center = 15
            y_center = 15
            radius = 5
            end_angle = self.angle + 180 # Half circle for the loading effect
        
            # Circle Segment
            self.canvas.create_arc(
                x_center - radius,
                y_center - radius,
                x_center + radius,
                y_center + radius,
                start = self.angle,
                extent = 180,
                fill = "white"
            )
        
            # Update the angle for next time
            self.angle += 10
            if self.angle >= 360:
                self.angle = 0
        
            self.after(50, self.update_circle)
    
    def show_dashboard(self,username):
        self.reset_form()
        # Hide current frame and open the dashboard
        self.hide()
        dashboard = Dashboard(self.main_app, username)
        dashboard.pack(fill='both', expand=True)
    
    def hide(self):
        self.pack_forget()  # Use pack_forget to hide the current screen
        
    def reset_form(self):
        # Clear all input fields and reset error messages
        self.username_entry.delete(0, "end")    # Clear the username
        self.password_entry.delete(0, "end")    # Clear the password
        self.update_console("")                 # Clear console
        self.is_loading = False                 # Stop the loading circle
        self.canvas.delete("all")               # Clear the loading circle
        
    def on_show(self):
        self.reset_form()
        self.password_entry.configure(show="*") # Ensure password is hidden
        self.is_loading = False
        self.canvas.delete("all")

if __name__ == "__main__":
    pass
