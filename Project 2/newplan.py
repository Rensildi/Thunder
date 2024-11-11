from customtkinter import CTkToplevel, CTkLabel, CTkEntry, CTkButton, CTkTextbox, CTkFrame, CTkScrollableFrame
from database import insert_business_plan, update_business_plan, check_business_name_exists
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

safety_setting = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_SECUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
]

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config,
  system_instruction="You are an advanced AI specializing in business planning and strategy development...",
)

history = []

class BusinessPlanForm(CTkToplevel):
    def __init__(self, master, username, business_name=None, description="", goals="", target_audience=""):
        super().__init__(master)
        self.username = username
        self.original_business_name = business_name
        self.title("Business Plan" if not business_name else "Edit Business Plan")
        self.geometry("1000x600")  # Adjusted for side-by-side layout

        # Container frame to hold both form and AI chat frames side by side
        self.container_frame = CTkFrame(self)
        self.container_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Main frames for side-by-side layout within container_frame
        self.form_frame = CTkFrame(self.container_frame, width=500)
        self.form_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        self.ai_frame = CTkFrame(self.container_frame, width=500)
        self.ai_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Add a scrollable frame to form_frame for the business plan form
        self.scrollable_form_frame = CTkScrollableFrame(self.form_frame, width=480, height=450)
        self.scrollable_form_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Determine if user is editing or creating a business plan
        if business_name:
            self.initialize_edit_form(description, goals, target_audience)
        else:
            self.initialize_create_form()

        # Initialize AI Chat section
        self.initialize_ai_chat()

        # Submit Button
        self.submit_button = CTkButton(self.form_frame, text="Submit", command=self.submit_business_plan)
        self.submit_button.pack(pady=10)

    def initialize_create_form(self):
        """Show form for creating a new business plan"""

        # Configure the column to expand
        self.scrollable_form_frame.grid_columnconfigure(0, weight=1)

        CTkLabel(self.scrollable_form_frame, text="Business Name:", font=("Arial", 14)).grid(row=0, column=0, sticky="w", padx=(5, 10), pady=0)
        self.name_entry = CTkTextbox(self.scrollable_form_frame, height=20, wrap="word")
        self.name_entry.grid(row=1, column=0, padx=5, pady=5, sticky="ew", columnspan=2)

        CTkLabel(self.scrollable_form_frame, text="Description:", font=("Arial", 14)).grid(row=2, column=0, sticky="w", padx=(5, 10), pady=0)
        self.description_entry = CTkTextbox(self.scrollable_form_frame, height=100, wrap="word")
        self.description_entry.grid(row=3, column=0, padx=5, pady=5, sticky="ew", columnspan=2)

        CTkLabel(self.scrollable_form_frame, text="Goals:", font=("Arial", 14)).grid(row=4, column=0, sticky="w", padx=(5, 10), pady=0)
        self.goals_entry = CTkTextbox(self.scrollable_form_frame, height=100, wrap="word")
        self.goals_entry.grid(row=5, column=0, padx=5, pady=5, sticky="ew", columnspan=2)

        CTkLabel(self.scrollable_form_frame, text="Mission Statement:", font=("Arial", 14)).grid(row=6, column=0, sticky="w", padx=(5, 10), pady=0)
        self.mission_entry = CTkTextbox(self.scrollable_form_frame, height=100, wrap="word")
        self.mission_entry.grid(row=7, column=0, padx=5, pady=5, sticky="ew", columnspan=2)

        CTkLabel(self.scrollable_form_frame, text="Projected Earnings:", font=("Arial", 14)).grid(row=8, column=0, sticky="w", padx=(5, 10), pady=0)
        self.earnings_entry = CTkTextbox(self.scrollable_form_frame, height=100, wrap="word")
        self.earnings_entry.grid(row=9, column=0, padx=5, pady=5, sticky="ew", columnspan=2)

        CTkLabel(self.scrollable_form_frame, text="Marketing Strategy:", font=("Arial", 14)).grid(row=10, column=0, sticky="w", padx=(5, 10), pady=0)
        self.marketing_entry = CTkTextbox(self.scrollable_form_frame, height=100, wrap="word")
        self.marketing_entry.grid(row=11, column=0, padx=5, pady=5, sticky="ew", columnspan=2)

        CTkLabel(self.scrollable_form_frame, text="Budget:", font=("Arial", 14)).grid(row=12, column=0, sticky="w", padx=(5, 10), pady=0)
        self.budget_entry = CTkTextbox(self.scrollable_form_frame, height=100, wrap="word")
        self.budget_entry.grid(row=13, column=0, padx=5, pady=5, sticky="ew", columnspan=2)
        
    def initialize_edit_form(self, description, goals, target_audience):
        """Show form for editing a plan"""
        # Configure the column to expand
        self.scrollable_form_frame.grid_columnconfigure(0, weight=1)

        CTkLabel(self.scrollable_form_frame, text="Business Name:", font=("Arial", 14)).grid(row=0, column=0, sticky="w", padx=(5, 10), pady=0)
        self.name_entry = CTkTextbox(self.scrollable_form_frame, height=20, wrap="word")
        self.name_entry.grid(row=1, column=0, padx=5, pady=5, sticky="ew", columnspan=2)
        self.name_entry.insert(0, self.original_business_name)

        CTkLabel(self.scrollable_form_frame, text="Description:", font=("Arial", 14)).grid(row=2, column=0, sticky="w", padx=(5, 10), pady=0)
        self.description_entry = CTkTextbox(self.scrollable_form_frame, height=100, wrap="word")
        self.description_entry.grid(row=3, column=0, padx=5, pady=5, sticky="ew", columnspan=2)
        self.description_entry.insert(0, description)

        CTkLabel(self.scrollable_form_frame, text="Goals:", font=("Arial", 14)).grid(row=4, column=0, sticky="w", padx=(5, 10), pady=0)
        self.goals_entry = CTkTextbox(self.scrollable_form_frame, height=100, wrap="word")
        self.goals_entry.grid(row=5, column=0, padx=5, pady=5, sticky="ew", columnspan=2)
        self.goals_entry.insert(0, goals)

        CTkLabel(self.scrollable_form_frame, text="Mission Statement:", font=("Arial", 14)).grid(row=6, column=0, sticky="w", padx=(5, 10), pady=0)
        self.mission_entry = CTkTextbox(self.scrollable_form_frame, height=100, wrap="word")
        self.mission_entry.grid(row=7, column=0, padx=5, pady=5, sticky="ew", columnspan=2)
        self.mission_entry.insert(0, self.original_business_name)

        CTkLabel(self.scrollable_form_frame, text="Projected Earnings:", font=("Arial", 14)).grid(row=8, column=0, sticky="w", padx=(5, 10), pady=0)
        self.earnings_entry = CTkTextbox(self.scrollable_form_frame, height=100, wrap="word")
        self.earnings_entry.grid(row=9, column=0, padx=5, pady=5, sticky="ew", columnspan=2)
        self.earnings_entry.insert(0, description)

        CTkLabel(self.scrollable_form_frame, text="Marketing Strategy:", font=("Arial", 14)).grid(row=10, column=0, sticky="w", padx=(5, 10), pady=0)
        self.marketing_entry = CTkTextbox(self.scrollable_form_frame, height=100, wrap="word")
        self.marketing_entry.grid(row=11, column=0, padx=5, pady=5, sticky="ew", columnspan=2)
        self.marketing_entry.insert(0, goals)

        CTkLabel(self.scrollable_form_frame, text="Budget:", font=("Arial", 14)).grid(row=12, column=0, sticky="w", padx=(5, 10), pady=0)
        self.budget_entry = CTkTextbox(self.scrollable_form_frame, height=100, wrap="word")
        self.budget_entry.grid(row=13, column=0, padx=5, pady=5, sticky="ew", columnspan=2)
        self.budget_entry.insert(0, target_audience)

    def initialize_ai_chat(self):
        """Initialize the AI Chat section in ai_frame"""
        # Chat box
        self.chat_box = CTkTextbox(self.ai_frame, width=380, height=442, state='disabled')
        self.chat_box.pack(pady=10)

        # User input
        self.user_input = CTkEntry(self.ai_frame, width=380)
        self.user_input.pack(pady=10)
        self.user_input.bind("<Return>", self.send_message)

        # Send button
        self.send_button = CTkButton(self.ai_frame, text="Send", command=self.send_message)
        self.send_button.pack(pady=10)

    def submit_business_plan(self):
        # Collect data from form fields
        new_business_name = self.name_entry.get()
        description = self.description_entry.get()
        goals = self.goals_entry.get()
        target_audience = self.target_audience_entry.get()

        if self.original_business_name:
            if new_business_name != self.original_business_name:
                if check_business_name_exists(new_business_name):
                    print(f"Business name '{new_business_name}' already exists. Choose a different name.")
                    return

            update_business_plan(self.original_business_name, new_business_name, description, goals, target_audience)
            print("Business Plan Updated in Database")
        else:
            insert_business_plan(self.username, new_business_name, description, goals, target_audience)
            print("Business Plan Submitted and Saved to Database")

        self.master.load_business_plans()
        self.destroy()

    def send_message(self, event=None):
        user_message = self.user_input.get()

        if user_message.lower() == "exit":
            self.quit()

        self.chat_box.configure(state='normal')
        self.chat_box.insert('end', f"You: {user_message}\n\n") 
        self.chat_box.configure(state='disabled')
        self.chat_box.yview('end')

        self.user_input.delete(0, 'end')

        # Generate response from Gemini
        chat_session = model.start_chat(history=history)
        response = chat_session.send_message(user_message)
        model_response = response.text

        self.chat_box.configure(state='normal')
        self.chat_box.insert('end', f"\nBot: {model_response}\n\n") 
        self.chat_box.configure(state='disabled')
        self.chat_box.yview('end')

        # Update history
        history.append({"role": "user", "parts": [f"\n\n{user_message}\n\n"]})
        history.append({"role": "model", "parts": [f"\n\n{model_response}\n\n"]})
