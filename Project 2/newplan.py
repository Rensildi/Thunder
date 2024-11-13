from customtkinter import CTkToplevel, CTkLabel, CTkEntry, CTkButton, CTkTextbox, CTkFrame, CTkScrollableFrame, CTkImage
from database import insert_business_plan, update_business_plan, check_business_name_exists, get_business_plan_data
import os
import google.generativeai as genai
from dotenv import load_dotenv
from tkinter import Toplevel, filedialog, messagebox, Button
from io import BytesIO
from pdf import BusinessPlanPDFGenerator
from reportlab.pdfgen import canvas
from PIL import Image, ImageTk
from CTkMessagebox import CTkMessagebox
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

# Load the question mark image
question_mark_image = Image.open("images/help-icon.png")
question_mark_image = question_mark_image.resize((20, 20), Image.Resampling.LANCZOS)
question_mark_ctk_image = CTkImage(light_image=question_mark_image, dark_image=question_mark_image, size=(20, 20))

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

        # Save Button
        self.submit_button = CTkButton(self.form_frame, text="Save", command=self.submit_business_plan)
        self.submit_button.pack(pady=10)

        # Create PDF Button
        self.create_pdf_button = CTkButton(self.form_frame, text="Create PDF", command=self.create_pdf)
        self.create_pdf_button.pack(pady=10)

    def help_explanation(self, message, event=None):
      CTkMessagebox(title="Explanation", message=message, icon="info")
    
    def initialize_create_form(self):
        """Show form for creating a new business plan"""
        # Configure the column to expand
        self.scrollable_form_frame.grid_columnconfigure(0, weight=1)
        
        CTkLabel(self.scrollable_form_frame, text="Business Name:", font=("Arial", 14)).grid(row=0, column=0, sticky="w", padx=(5, 10), pady=0)
        help_icon_label = CTkLabel(self.scrollable_form_frame, text="", image=question_mark_ctk_image)
        help_icon_label.grid(row=0, column=1, sticky="e", padx=(5,10), pady=0)
        help_icon_label.bind("<Button-1>", lambda e: self.help_explanation("What would you like to call your business? Choose a name that reflects its purpose and stands out to your audience"))
        self.name_entry = CTkTextbox(self.scrollable_form_frame, height=20, wrap="word")
        self.name_entry.grid(row=1, column=0, padx=5, pady=5, sticky="ew", columnspan=2)
        
        CTkLabel(self.scrollable_form_frame, text="Description:", font=("Arial", 14)).grid(row=2, column=0, sticky="w", padx=(5, 10), pady=0)
        help_icon_label = CTkLabel(self.scrollable_form_frame, text="", image=question_mark_ctk_image)
        help_icon_label.grid(row=2, column=1, sticky="e", padx=(5,10), pady=0)
        help_icon_label.bind("<Button-1>", lambda e: self.help_explanation("Describe your business. What products or services do you offer? What problem does your business solve, and how does it add value to customers?"))
        self.description_entry = CTkTextbox(self.scrollable_form_frame, height=100, wrap="word")
        self.description_entry.grid(row=3, column=0, padx=5, pady=5, sticky="ew", columnspan=2)
        
        CTkLabel(self.scrollable_form_frame, text="Goals:", font=("Arial", 14)).grid(row=4, column=0, sticky="w", padx=(5, 10), pady=0)
        help_icon_label = CTkLabel(self.scrollable_form_frame, text="", image=question_mark_ctk_image)
        help_icon_label.grid(row=4, column=1, sticky="e", padx=(5,10), pady=0)
        help_icon_label.bind("<Button-1>", lambda e: self.help_explanation("What are the key objectives for your business? Think about both short-term and long-term goals that will help guide its growth and success."))
        self.goals_entry = CTkTextbox(self.scrollable_form_frame, height=100, wrap="word")
        self.goals_entry.grid(row=5, column=0, padx=5, pady=5, sticky="ew", columnspan=2)
        
        CTkLabel(self.scrollable_form_frame, text="Mission Statement:", font=("Arial", 14)).grid(row=6, column=0, sticky="w", padx=(5, 10), pady=0)
        help_icon_label = CTkLabel(self.scrollable_form_frame, text="", image=question_mark_ctk_image)
        help_icon_label.grid(row=6, column=1, sticky="e", padx=(5,10), pady=0)
        help_icon_label.bind("<Button-1>", lambda e: self.help_explanation("Summarize the purpose and core values of your business. What drives your business, and what impact do you want to make on customers and the community?"))
        self.mission_entry = CTkTextbox(self.scrollable_form_frame, height=100, wrap="word")
        self.mission_entry.grid(row=7, column=0, padx=5, pady=5, sticky="ew", columnspan=2)
        
        CTkLabel(self.scrollable_form_frame, text="Projected Earnings:", font=("Arial", 14)).grid(row=8, column=0, sticky="w", padx=(5, 10), pady=0)
        help_icon_label = CTkLabel(self.scrollable_form_frame, text="", image=question_mark_ctk_image)
        help_icon_label.grid(row=8, column=1, sticky="e", padx=(5,10), pady=0)
        help_icon_label.bind("<Button-1>", lambda e: self.help_explanation("Estimate the financial potential of your business. Include expected revenue and profits over specific periods to help guide planning and investments."))
        self.earnings_entry = CTkTextbox(self.scrollable_form_frame, height=100, wrap="word")
        self.earnings_entry.grid(row=9, column=0, padx=5, pady=5, sticky="ew", columnspan=2)
        
        CTkLabel(self.scrollable_form_frame, text="Marketing Strategy:", font=("Arial", 14)).grid(row=10, column=0, sticky="w", padx=(5, 10), pady=0)
        help_icon_label = CTkLabel(self.scrollable_form_frame, text="", image=question_mark_ctk_image)
        help_icon_label.grid(row=10, column=1, sticky="e", padx=(5,10), pady=0)
        help_icon_label.bind("<Button-1>", lambda e: self.help_explanation("Describe how you'll promote your business to reach your target audience. Consider channels like social media, advertising, partnerships, and other tactics to attract and retain customers."))
        self.marketing_entry = CTkTextbox(self.scrollable_form_frame, height=100, wrap="word")
        self.marketing_entry.grid(row=11, column=0, padx=5, pady=5, sticky="ew", columnspan=2)
        
        CTkLabel(self.scrollable_form_frame, text="Budget:", font=("Arial", 14)).grid(row=12, column=0, sticky="w", padx=(5, 10), pady=0)
        help_icon_label = CTkLabel(self.scrollable_form_frame, text="", image=question_mark_ctk_image)
        help_icon_label.grid(row=12, column=1, sticky="e", padx=(5,10), pady=0)
        help_icon_label.bind("<Button-1>", lambda e: self.help_explanation("Outline the financial resources required for your business. Include expenses like production, marketing, operations, and other costs to maintain financial stability."))
        self.budget_entry = CTkTextbox(self.scrollable_form_frame, height=100, wrap="word")
        self.budget_entry.grid(row=13, column=0, padx=5, pady=5, sticky="ew", columnspan=2)
        
    def initialize_edit_form(self, description, goals, target_audience):
        """Show form for editing a plan"""
        # Configure the column to expand
        self.scrollable_form_frame.grid_columnconfigure(0, weight=1)

        CTkLabel(self.scrollable_form_frame, text="Business Name:", font=("Arial", 14)).grid(row=0, column=0, sticky="w", padx=(5, 10), pady=0)
        self.name_entry = CTkTextbox(self.scrollable_form_frame, height=20, wrap="word")
        self.name_entry.grid(row=1, column=0, padx=5, pady=5, sticky="ew", columnspan=2)
        self.name_entry.insert("1.0", self.original_business_name)

        CTkLabel(self.scrollable_form_frame, text="Description:", font=("Arial", 14)).grid(row=2, column=0, sticky="w", padx=(5, 10), pady=0)
        self.description_entry = CTkTextbox(self.scrollable_form_frame, height=100, wrap="word")
        self.description_entry.grid(row=3, column=0, padx=5, pady=5, sticky="ew", columnspan=2)
        self.description_entry.insert("1.0", description)

        CTkLabel(self.scrollable_form_frame, text="Goals:", font=("Arial", 14)).grid(row=4, column=0, sticky="w", padx=(5, 10), pady=0)
        self.goals_entry = CTkTextbox(self.scrollable_form_frame, height=100, wrap="word")
        self.goals_entry.grid(row=5, column=0, padx=5, pady=5, sticky="ew", columnspan=2)
        self.goals_entry.insert("1.0", goals)

        CTkLabel(self.scrollable_form_frame, text="Target Audience:", font=("Arial", 14)).grid(row=6, column=0, sticky="w", padx=(5, 10), pady=0)
        self.target_audience_entry = CTkTextbox(self.scrollable_form_frame, height=100, wrap="word")
        self.target_audience_entry.grid(row=7, column=0, padx=5, pady=5, sticky="ew", columnspan=2)
        self.target_audience_entry.insert("1.0", target_audience)

        CTkLabel(self.scrollable_form_frame, text="Mission Statement:", font=("Arial", 14)).grid(row=8, column=0, sticky="w", padx=(5, 10), pady=0)
        self.mission_entry = CTkTextbox(self.scrollable_form_frame, height=100, wrap="word")
        self.mission_entry.grid(row=9, column=0, padx=5, pady=5, sticky="ew", columnspan=2)
        self.mission_entry.insert("1.0", self.original_business_name)

        CTkLabel(self.scrollable_form_frame, text="Projected Earnings:", font=("Arial", 14)).grid(row=10, column=0, sticky="w", padx=(5, 10), pady=0)
        self.earnings_entry = CTkTextbox(self.scrollable_form_frame, height=100, wrap="word")
        self.earnings_entry.grid(row=11, column=0, padx=5, pady=5, sticky="ew", columnspan=2)
        self.earnings_entry.insert("1.0", description)

        CTkLabel(self.scrollable_form_frame, text="Marketing Strategy:", font=("Arial", 14)).grid(row=12, column=0, sticky="w", padx=(5, 10), pady=0)
        self.marketing_entry = CTkTextbox(self.scrollable_form_frame, height=100, wrap="word")
        self.marketing_entry.grid(row=13, column=0, padx=5, pady=5, sticky="ew", columnspan=2)
        self.marketing_entry.insert("1.0", goals)

        CTkLabel(self.scrollable_form_frame, text="Budget:", font=("Arial", 14)).grid(row=14, column=0, sticky="w", padx=(5, 10), pady=0)
        self.budget_entry = CTkTextbox(self.scrollable_form_frame, height=100, wrap="word")
        self.budget_entry.grid(row=15, column=0, padx=5, pady=5, sticky="ew", columnspan=2)
        self.budget_entry.insert("1.0", target_audience)

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
        new_business_name = self.name_entry.get("1.0", "end").strip()
        description = self.description_entry.get("1.0", "end").strip()
        goals = self.goals_entry.get("1.0", "end").strip()
        target_audience = self.target_audience_entry.get("1.0", "end").strip()

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

    def create_pdf(self):
        """Create the business plan PDF and preview it in the system's default viewer"""
        # Get data from the form to create the business plan
        business_plan_data = get_business_plan_data(self.username, self.original_business_name)

        if business_plan_data:
            # Generate the PDF using the BusinessPlanPDFGenerator class
            pdf_generator = BusinessPlanPDFGenerator(business_plan_data)
            pdf_file = pdf_generator.generate_pdf()

            # Call the method to preview the PDF externally
            self.preview_pdf(pdf_file)
        else:
            messagebox.showerror("Error", "Could not fetch business plan data.")

    def preview_pdf(self, pdf_file):
        """Preview the pdf using default PDF viewer"""
        # Create a temporary file path for saving PDF
        temp_file_path = os.path.join(os.path.expanduser("~"), "business_plan_preview.pdf")

        # Save PDF to the temporary file
        with open(temp_file_path, "wb") as f:
            f.write(pdf_file.read())

        # Open PDF using system's default viewer
        os.startfile(temp_file_path)
