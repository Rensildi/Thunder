from customtkinter import *
import mysql.connector
import bcrypt  # Make sure to install bcrypt: pip install bcrypt
import createuser

class SignUp(CTk):
    def __init__(self):
        super().__init__()

        self.geometry("900x600")
        self.title("Thunder")

        self.create_widgets()

    def create_widgets(self):
        self.widget_welcome_section()
        self.widget_username_section()
        self.widget_password_section()
        self.widget_sign_up_button()
        self.widget_alternative_sign_up_button()

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
        self.username_asterisk.place(relx=0.6, rely=0.22)

        # Username entry
        self.username_entry = CTkEntry(master=self, placeholder_text="Username", width=300)
        self.username_entry.place(relx=0.7, rely=0.28, anchor="center")

        # Username requirements
        self.username_requirements = CTkLabel(
            master=self,
            text="Required 150 characters or less. Letters digits and @/./+/-/_ only",
            text_color="grey"
        )
        self.username_requirements.place(relx=0.536, rely=0.3)

    def widget_password_section(self):
        # Password label
        self.password_label = CTkLabel(master=self, text="Password")
        self.password_label.place(relx=0.536, rely=0.38)

        # Asterisk for password
        self.password_asterisk = CTkLabel(master=self, text='*', text_color="red")
        self.password_asterisk.place(relx=0.6, rely=0.38)

        # Password entry
        self.password_entry = CTkEntry(master=self, placeholder_text="Password", show="*", width=300)
        self.password_entry.place(relx=0.7, rely=0.44, anchor="center")

        # Password requirements
        self.password_requirements = CTkLabel(
            master=self,
            text="Your password can't be too similar to your other personal info.\n"
                 "Your password must contain at least 8 characters.\n"
                 "Your password can't be a commonly used password.\n"
                 "Your password can't be entirely numeric.",
            justify='left',
            text_color="grey",
            width=300
        )
        self.password_requirements.place(relx=0.536, rely=0.52, anchor='w')

        # Confirm Password Label
        self.confirm_password_label = CTkLabel(master=self, text="Confirm Password")
        self.confirm_password_label.place(relx=0.536, rely=0.6)

        # Asterisk for confirm password
        self.confirm_password_asterisk = CTkLabel(master=self, text='*', text_color="red")
        self.confirm_password_asterisk.place(relx=0.654, rely=0.6)

        # Confirm Password entry
        self.confirm_password_entry = CTkEntry(master=self, placeholder_text="Confirm Password", show="*", width=300)
        self.confirm_password_entry.place(relx=0.7, rely=0.66, anchor="center")

        # Confirm Password requirements
        self.confirm_password_requirements = CTkLabel(
            master=self,
            text="Enter the same Password as before",
            text_color="grey"
        )
        self.confirm_password_requirements.place(relx=0.536, rely=0.71, anchor="w")

    def widget_sign_up_button(self):
        # Sign Up button
        self.sign_up_button = CTkButton(master=self, text="Sign Up", width=300, height=30, command=self.sign_up)
        self.sign_up_button.place(relx=0.7, rely=0.8, anchor="center")

    def widget_alternative_sign_up_button(self):
        # Alternative sign up Google button
        self.continue_google_button = CTkButton(master=self, text="Continue With Google", width=300, height=30)
        self.continue_google_button.place(relx=0.7, rely=0.868, anchor="center")

    def sign_up(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        # Validate inputs
        if not username or not password or not confirm_password:
            print("All fields are required!")
            return
        if password != confirm_password:
            print("Passwords do not match!")
            return
        if len(password) < 8:
            print("Password must be at least 8 characters long!")
            return

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Call the create_user function to insert into the database
        createuser.create_user(username, hashed_password)

if __name__ == "__main__":
    app = SignUp()
    app.mainloop()
