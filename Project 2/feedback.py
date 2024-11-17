from customtkinter import *
import requests
from tkinter import messagebox
import os
from dotenv import load_dotenv

load_dotenv()
FORM_ENDPOINT = os.getenv("FORM_ENDPOINT")


class FeedbackForm(CTkToplevel):
    def __init__(self, dashboard, id, email, username):
        super().__init__()
        self.dashboard = dashboard  # Reference to the Dashboard instance
        self.id = id
        self.email = email
        self.username = username
        
        
        self.geometry("400x300")
        self.title("Submit Feedback")
        self.create_widgets()

    def create_widgets(self):
        CTkLabel(self, text="We value your feedback!", font=("Arial", 16)).pack(pady=10)

        # Feedback entry
        self.feedback_text = CTkTextbox(self, height=8, width=350)
        self.feedback_text.pack(pady=10)

        # Submit button
        submit_button = CTkButton(self, text="Submit", command=self.submit_feedback)
        submit_button.pack(pady=10)

    def submit_feedback(self):
        feedback_content = self.feedback_text.get("1.0", "end").strip()

        if not feedback_content:
            messagebox.showwarning("Empty Feedback", "Please write your feedback before submitting.")
            return
        
        # Data preparing to send to Formspree
        feedback_data = {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "feedback": feedback_content
        }

        # Send feedback via Formspree
        try:
            response = requests.post(FORM_ENDPOINT, json= feedback_data)

            if response.status_code == 200:
                messagebox.showinfo("Success", "Thank you for your feedback!")
                self.destroy()  # Close feedback window
            else:
                messagebox.showerror("Error", f"Failed to submit feedback: {response.status_code}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
