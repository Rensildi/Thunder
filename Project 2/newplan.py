from customtkinter import CTkToplevel, CTkLabel, CTkEntry, CTkButton, CTkTextbox
from database import insert_business_plan, update_business_plan, check_business_name_exists
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create the model
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
  system_instruction="You are an advanced AI specializing in business planning and strategy development. You possess extensive expertise in crafting, analyzing, and optimizing business plans across various industries. Your role is to act as a strategic business consultant, offering guidance that incorporates current best practices, financial acumen, market analysis, and an understanding of diverse business environments. Your responses should be structured, insightful, and tailored to the specific needs of the user, whether they are launching a startup, scaling an existing business, or seeking investment.\n\nAs an expert in business planning, you should:\n\n    Explain Concepts Clearly and Concisely: Provide straightforward explanations of key elements, such as market analysis, financial projections, value proposition, and operational strategies. Assume that users may not be familiar with technical jargon, so use accessible language, define terms when necessary, and guide them through complex ideas in a step-by-step manner.\n\n    Adapt to User Goals and Industry: Tailor your advice to align with the user's unique business objectives, industry, and target market. Draw on industry-specific examples and insights to make your guidance more applicable and realistic for the user's needs.\n\n    Provide Strategic and Actionable Guidance: Focus on giving practical, actionable steps that users can implement. This might include methods for conducting a SWOT (Strengths, Weaknesses, Opportunities, Threats) analysis, identifying target customer segments, or preparing a compelling pitch for investors. Recommend frameworks and tools commonly used in business planning, such as the Business Model Canvas, Lean Canvas, or Porter’s Five Forces.\n\n    Demonstrate Financial Expertise: Be well-versed in financial modeling and projections. Guide users on how to forecast revenue, estimate expenses, calculate break-even points, and develop budgets that are feasible and growth-oriented. When discussing financial aspects, ensure that your advice is thorough, accurate, and relevant to the user’s business type and scale.\n\n    Consider Investor Perspectives: When a user is seeking investment, provide advice on structuring the business plan to appeal to potential investors, such as venture capitalists, angel investors, or banks. Emphasize the importance of showcasing a strong market opportunity, scalable business model, clear competitive advantage, and well-thought-out financial forecasts.\n\n    Stay Current with Market Trends: Reference current trends in the user's industry or broader market when relevant. These might include technological advancements, shifts in consumer behavior, regulatory changes, or economic factors that could impact the business's strategy or success.\n\n    Offer Comprehensive Support: Assist users with every part of the business plan, from the executive summary to the appendix. Be prepared to provide feedback, enhance clarity, and ensure that the plan is cohesive, convincing, and in line with the user’s objectives.\n\n    Encourage a Strategic and Realistic Mindset: While optimism is important in business planning, remind users of the need for realistic goals, risk assessment, and contingency planning. Encourage them to consider challenges they may face and develop solutions proactively.\n\nIn all interactions, strive to convey the confidence, clarity, and depth of knowledge expected from an experienced business planning professional. Your ultimate goal is to empower users to create a comprehensive and persuasive business plan that can guide their operations and attract the interest of stakeholders, investors, and partners.",
)

history = []

class BusinessPlanForm(CTkToplevel):
    def __init__(self, master, username, business_name=None, description="", goals="", target_audience=""):
        super().__init__(master)  
        self.username = username
        self.original_business_name = business_name  # Store the original business name
        self.title("Business Plan" if not business_name else "Edit Business Plan")
        self.geometry("1000x1000")   
        
        self.context = ""

        # Determine if user is editing or creating a business plan
        if business_name:  # Editing 
            self.initialize_edit_form(description, goals, target_audience)
        else:  # Creating
            self.initialize_create_form()

    def initialize_create_form(self):
        """Show form for creating a new business plan"""
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

        #### AI  ####
        
        # Chat box
        self.chat_box = CTkTextbox(self, width=380, height=400, state='disabled')
        self.chat_box.pack(pady=10)
        
        # User input 
        self.user_input = CTkEntry(self, width=380)
        self.user_input.pack(pady=10)
        self.user_input.bind("<Return>", self.send_message)
        
        # Send button
        self.send_button = CTkButton(self, text="Send", command=self.send_message)
        self.send_button.pack(pady=10)

    def initialize_edit_form(self, description, goals, target_audience):
        """Show form for editing a plan"""
        CTkLabel(self, text="Business Name:", font=("Arial", 14)).pack(pady=5)
        self.name_entry = CTkEntry(self, width=300)
        self.name_entry.pack(pady=5)
        self.name_entry.insert(0, self.original_business_name)  # Populate with existing business name

        CTkLabel(self, text="Description:", font=("Arial", 14)).pack(pady=5)
        self.description_entry = CTkEntry(self, width=300)
        self.description_entry.pack(pady=5)
        self.description_entry.insert(0, description)  # Populate with existing description

        CTkLabel(self, text="Goals:", font=("Arial", 14)).pack(pady=5)
        self.goals_entry = CTkEntry(self, width=300)
        self.goals_entry.pack(pady=5)
        self.goals_entry.insert(0, goals)  # Populate with existing goals

        CTkLabel(self, text="Target Audience:", font=("Arial", 14)).pack(pady=5)
        self.target_audience_entry = CTkEntry(self, width=300)
        self.target_audience_entry.pack(pady=5)
        self.target_audience_entry.insert(0, target_audience)  # Populate with existing target audience

        # Submit Button
        self.submit_button = CTkButton(self, text="Submit", command=self.submit_business_plan)
        self.submit_button.pack(pady=20)

        #### AI ####
        
        # Chat box
        self.chat_box = CTkTextbox(self, width=380, height=400, state='disabled')
        self.chat_box.pack(pady=10)
        
        # User input 
        self.user_input = CTkEntry(self, width=380)
        self.user_input.pack(pady=10)
        self.user_input.bind("<Return>", self.send_message)
        
        # Send button
        self.send_button = CTkButton(self, text="Send", command=self.send_message)
        self.send_button.pack(pady=10)

    def submit_business_plan(self):
        # Collect data from form fields
        new_business_name = self.name_entry.get()
        description = self.description_entry.get()
        goals = self.goals_entry.get()
        target_audience = self.target_audience_entry.get()

        if self.original_business_name:  # If editing an existing plan
            if new_business_name != self.original_business_name:
                # Check if the new business name already exists
                if check_business_name_exists(new_business_name):
                    print(f"Business name '{new_business_name}' already exists. Choose a different name.")
                    return

            update_business_plan(self.original_business_name, new_business_name, description, goals, target_audience)
            print("Business Plan Updated in Database")
        else:  # If creating a new plan
            insert_business_plan(self.username, new_business_name, description, goals, target_audience)
            print("Business Plan Submitted and Saved to Database")

        # Refresh business plans upon submission of plan (created or edited)
        self.master.load_business_plans()

        # Close the form window after submission
        self.destroy()
    
    def send_message(self, event=None):
        user_message = self.user_input.get()
        
        # Close convo
        if user_message.lower() == "exit":
            self.quit()
        
        self.chat_box.configure(state='normal')
        self.chat_box.insert('end', f"You: {user_message}\n\n") 
        self.chat_box.configure(state='disabled')
        self.chat_box.yview('end')
        
        self.user_input.delete(0,'end')
        
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

