from customtkinter import *

class Dashboard(CTkFrame):
    def __init__(self, main_app, username):
        super().__init__(master=main_app.root)  # Set the main app's root as the master
        self.main_app = main_app  # Store reference to the main app
        self.username = username  # Store the username
        
        self.create_widgets()  # Call method to create widgets

    def create_widgets(self):
        
        # Dashboard Label
        self.label = CTkLabel(self, text=f"Welcome to the Dashboard, {self.username}!", font=("Arial", 24))
        self.label.pack(pady=20)

        # Add additional dashboard components here if needed
        
        # Logout Button
        self.logout_button = CTkButton(self,text="Logout", command=self.logout)
        self.logout_button.pack(pady=10)
        
    def logout(self):
        self.pack_forget()
        self.main_app.show_signin()

if __name__=="__main__":
    pass  # The main application will handle the instantiation
