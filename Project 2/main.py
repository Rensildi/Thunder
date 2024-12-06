from customtkinter import *
from database import initialize_db
from SignIn import SignIn
from SignUp import SignUp
import threading
import os
import signal
from supabase import *
import onboarding_screen1
import onboarding_screen2
import onboarding_screen3

class MainApp:
    def __init__(self):
        """Initialize main app"""
        print("Initializing MainApp")  
        self.root = CTk()  # Create the main application window
        self.root.geometry("900x600")
        self.root.title("Thunder")

        SUPA_URL = os.getenv("SUPABASE_URL")
        SUPA_KEY = os.getenv("SUPABASE_KEY")
        self.supabase = create_client(SUPA_URL, SUPA_KEY)

        initialize_db()

        self.sign_in_screen = SignIn(self)  # Pass self
        self.sign_up_screen = SignUp(self)  # Pass self

        self.sign_in_screen.pack(fill='both', expand=True)  # Show sign in screen

    def run(self):
        """Run main app"""
        self.root.mainloop()
        
    def on_closing(self):
        """Shut down Google server"""
        # Shutting down the server if needed
        os.kill(os.getpid(), signal.SIGINT)
        #server_thread.join()  # Wait for server thread to finish
        self.root.destroy()

    def show_signin(self):
        """SHow sign in page"""
        self.sign_up_screen.pack_forget()  # Hide SignUp if it's open
        self.sign_in_screen.pack(fill='both', expand=True)  # Show SignIn
        self.sign_in_screen.on_show() #Call the on_show method to reset the from.

    def show_signup(self):
        """Show sign up page"""
        self.sign_in_screen.pack_forget()  # Hide SignIn if it's open
        self.sign_up_screen.pack(fill='both', expand=True)  # Show SignUp

    def show_onboarding1(self):
        """Display Onboarding Screen 1."""
        self.clear_screens()
        onboarding_screen1.run(self.root, self.show_onboarding2)

    def show_onboarding2(self):
        """Display Onboarding Screen 2."""
        self.clear_screens()
        onboarding_screen2.run(self.root, self.show_onboarding3)

    def show_onboarding3(self):
        """Display Onboarding Screen 3."""
        self.clear_screens()
        onboarding_screen3.run(self.root, self.exit_program)

    def exit_program(self):
        """Exit the program."""
        self.root.destroy()

    def clear_screens(self):
        """Hide all active screens before switching."""
        for widget in self.root.winfo_children():
            widget.pack_forget()
    

if __name__ == "__main__":
    app = MainApp()  # Create an instance of MainApp
    app.root.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.run()  # Run the application
