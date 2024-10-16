from customtkinter import *
from SignUp import SignUp
import createuser
import bcrypt


class SignIn(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("900x600")
        self.title("Thunder")

        self.create_widgets()

    def create_widgets(self):
        self.widget_welcome_section()
        self.widget_sign_in_button()
        self.widget_sign_up_button()
        self.widget_alternative_sign_in_button()

    def widget_welcome_section(self):
        # Welcome Label
        welcome_label = CTkLabel(master=self, text="Welcome Back", font=("Arial", 30))
        welcome_label.place(relx=0.7, rely=0.1, anchor="center")

        # Description Label
        description_label = CTkLabel(master=self, text="This is a description", font=("Arial", 14), text_color="grey")
        description_label.place(relx=0.7, rely=0.15, anchor="center")

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

    def launch_signup(self):
        self.destroy()
        signup_app = SignUp()
        signup_app.mainloop()

    def sign_in(self):
        # Implement sign-in functionality here
        print("Sign In button clicked")  # Placeholder for actual sign-in logic


if __name__ == "__main__":
    app = SignIn()
    app.mainloop()
