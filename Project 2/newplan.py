# business_plan_form.py

from customtkinter import CTkToplevel, CTkLabel, CTkEntry, CTkButton
from database import insert_business_plan

class BusinessPlanForm(CTkToplevel):
    def __init__(self, master, username):
        super().__init__(master)  
        self.username = username
        self.title("New Business Plan")
        self.geometry("400x500")  

        # Form Fields
        CTkLabel(self, text="Business Name:", font=("Arial", 14)).pack(pady=5)
        self.name_entry = CTkEntry(self, width=300)
        self.name_entry.pack(pady=5)

        CTkLabel(self, text="Description:", font=("Arial", 14)).pack(pady=5)
        self.description_entry = CTkEntry(self, width=300)
        self.description_entry.pack(pady=5)

        CTkLabel(self, text="Goals:", font=("Arial", 14)).pack(pady=5)
        self.goals_entry = CTkEntry(self, width=300)
        self.goals_entry.pack(pady=5)

        CTkLabel(self, text="Target Audience:", font=("Arial", 14)).pack(pady=5)
        self.target_audience_entry = CTkEntry(self, width=300)
        self.target_audience_entry.pack(pady=5)

        # Submit Button
        self.submit_button = CTkButton(self, text="Submit", command=self.submit_business_plan)
        self.submit_button.pack(pady=20)

    def submit_business_plan(self):
        # Collect data and perform submission logic here
        business_name = self.name_entry.get()
        description = self.description_entry.get()
        goals = self.goals_entry.get()
        target_audience = self.target_audience_entry.get()

        insert_business_plan(self.username, business_name, description, goals, target_audience)
        print("Business Plan Submitted and Saved to Database")

        # Close the form window after submission
        self.destroy()
