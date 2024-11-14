from tkinter import Tk
import onboarding_screen1  # Import the first onboarding screen


# Prototype main app to test the onboarding screens
class MainApp:
    def __init__(self):
        self.window = Tk()
        self.window.geometry("900x600")
        self.window.configure(bg="#105090")
        self.window.resizable(False, False)

    def run(self):
        # Start with the first onboarding screen
        onboarding_screen1.run(self.window)

    def start(self):
        # Start the app by running the main onboarding flow
        self.run()


# Create the MainApp instance and run the onboarding screens
if __name__ == "__main__":
    app = MainApp()
    app.start()