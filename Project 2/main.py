from customtkinter import *
from database import initialize_db
from SignIn import SignIn
from SignUp import SignUp
import threading
import os
import signal

class MainApp:
    def __init__(self):
        print("Initializing MainApp")  # Debugging statement
        self.root = CTk()  # Create the main application window
        self.root.geometry("900x600")
        self.root.title("Thunder")

        initialize_db()

        self.sign_in_screen = SignIn(self)  # Pass self
        self.sign_up_screen = SignUp(self)  # Pass self

        self.sign_in_screen.pack(fill='both', expand=True)  # Show sign in screen

    def run(self):
        self.root.mainloop()
        
    def on_closing(self):
        # Shutting down the server if needed
        os.kill(os.getpid(), signal.SIGINT)
        server_thread.join()  # Wait for server thread to finish
        self.root.destroy()

    def show_signin(self):
        self.sign_up_screen.pack_forget()  # Hide SignUp if it's open
        self.sign_in_screen.pack(fill='both', expand=True)  # Show SignIn

    def show_signup(self):
        self.sign_in_screen.pack_forget()  # Hide SignIn if it's open
        self.sign_up_screen.pack(fill='both', expand=True)  # Show SignUp

if __name__ == "__main__":
    # If you need to run a server, add that functionality here
    app = MainApp()  # Create an instance of MainApp
    app.root.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.run()  # Run the application
