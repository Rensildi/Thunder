from customtkinter import CTkToplevel, CTkLabel, CTkEntry, CTkButton, CTkTextbox, CTkFrame, CTkScrollableFrame, CTkImage
from database import insert_business_plan, update_business_plan, check_business_name_exists, get_business_plan_data, get_revenue_projection, get_market_share_projection
import awesometkinter
import os
import google.generativeai as genai
from dotenv import load_dotenv
from tkinter import Toplevel, filedialog, messagebox, Button
from io import BytesIO
from pdf import BusinessPlanPDFGenerator
from reportlab.pdfgen import canvas
from PIL import Image, ImageTk
from CTkMessagebox import CTkMessagebox
from database import resource_path
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
question_mark_image = Image.open(resource_path("images/help-icon.png"))
question_mark_image = question_mark_image.resize((20, 20), Image.Resampling.LANCZOS)
question_mark_ctk_image = CTkImage(light_image=question_mark_image, dark_image=question_mark_image, size=(20, 20))

class BusinessPlanForm(CTkToplevel):
    def __init__(self, master, username, business_name=None, industry="", employees="", legal_structure="", description="", mission_statement="", principal_members="", future="",
             products="", services="", pricing="", research="", industry_state="", competitors="", target_audience="",
             company_advantages="", regulations_compliance="", growth_strategy="", marketing_budget="", advertising_plan="",
             customer_interaction="", customer_retention="", bank="", accounting_firm="", financing_sought="", 
             profit_loss_statement="", break_even_analysis="", roi="", contingency_plan="", disaster_recovery_plan="",
             insurance_info="", name="", address="", city="", state="", zip_code="", phone="", email="", law_firm="", 
             intellectual_property=""):
        """Initialize the business plan form and ai chatbot"""
        super().__init__(master)
        self.username = username
        self.original_business_name = business_name
        self.title("Business Plan" if not business_name else "Edit Business Plan")
        self.geometry("1000x675")  # Adjusted for side-by-side layout

        # Container frame to hold both form and AI chat frames side by side
        self.container_frame = CTkFrame(self)
        self.container_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Main frames for side-by-side layout within container_frame
        self.form_frame = CTkFrame(self.container_frame, width=500)
        self.form_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        # Frame for Progress Tracker and AI Chat (right side)
        self.ai_container_frame = CTkFrame(self.container_frame, width=500)
        self.ai_container_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Progress Tracker Frame (above ai_frame)
        self.progress_tracker_frame = CTkFrame(self.ai_container_frame, height=80, width=500)
        self.progress_tracker_frame.pack(side="top", fill="x", padx=10, pady=(5, 0))

        self.ai_frame = CTkFrame(self.ai_container_frame, width=500)
        self.ai_frame.pack(side="top", fill="both", expand=True, padx=10, pady=(5, 10))
        
        CTkLabel(self.form_frame, text="Business Plan:", font=("Arial", 20)).pack(side="top", pady=(10, 0), anchor="center")
        CTkLabel(self.ai_frame, text="Business Assistant:", font=("Arial", 20)).pack(side="top", pady=(10, 0), anchor="center")
        

        # Add a scrollable frame to form_frame for the business plan form
        self.scrollable_form_frame = CTkScrollableFrame(self.form_frame, width=480, height=450)
        self.scrollable_form_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Determine if user is editing or creating a business plan
        if business_name:
            business_plan_data = get_business_plan_data(username, business_name)
            
            # business_plans table
            industry = business_plan_data['business_plans'][3] if business_plan_data['business_plans'] is not None else ""
            employees = business_plan_data['business_plans'][4] if business_plan_data['business_plans'] is not None else ""
            legal_structure = business_plan_data['business_plans'][5] if business_plan_data['business_plans'] is not None else ""

            # executive_summary table
            description = business_plan_data['executive_summary'][2] if business_plan_data['executive_summary'] is not None else ""
            mission_statement = business_plan_data['executive_summary'][3] if business_plan_data['executive_summary'] is not None else ""
            principal_members = business_plan_data['executive_summary'][4] if business_plan_data['executive_summary'] is not None else ""
            future = business_plan_data['executive_summary'][5] if business_plan_data['executive_summary'] and business_plan_data['executive_summary'][5] is not None else ""

            # market_research table
            industry_state = business_plan_data['market_research'][2] if business_plan_data['market_research'] is not None else ""
            competitors = business_plan_data['market_research'][3] if business_plan_data['market_research'] is not None else ""
            target_audience = business_plan_data['market_research'][4] if business_plan_data['market_research'] is not None else ""
            company_advantages = business_plan_data['market_research'][5] if business_plan_data['market_research'] is not None else ""
            regulations_compliance = business_plan_data['market_research'][6] if business_plan_data['market_research'] is not None else ""

            # marketing_strategy table
            growth_strategy = business_plan_data['marketing_strategy'][2] if business_plan_data['marketing_strategy'] is not None else ""
            advertising_plan = business_plan_data['marketing_strategy'][3] if business_plan_data['marketing_strategy'] is not None else ""
            marketing_budget = business_plan_data['marketing_strategy'][4] if business_plan_data['marketing_strategy'] is not None else ""
            customer_interaction = business_plan_data['marketing_strategy'][5] if business_plan_data['marketing_strategy'] is not None else ""
            customer_retention = business_plan_data['marketing_strategy'][6] if business_plan_data['marketing_strategy'] is not None else ""

            # service_line table
            products = business_plan_data['service_line'][2] if business_plan_data['service_line'] is not None else ""
            services = business_plan_data['service_line'][3] if business_plan_data['service_line'] is not None else ""
            pricing = business_plan_data['service_line'][4] if business_plan_data['service_line'] is not None else ""
            research = business_plan_data['service_line'][5] if business_plan_data['service_line'] is not None else ""

            # contact_information table
            name = business_plan_data['contact_information'][2] if business_plan_data['contact_information'] is not None else ""
            address = business_plan_data['contact_information'][3] if business_plan_data['contact_information'] is not None else ""
            city = business_plan_data['contact_information'][4] if business_plan_data['contact_information'] is not None else ""
            state = business_plan_data['contact_information'][5] if business_plan_data['contact_information'] is not None else ""
            zip_code = business_plan_data['contact_information'][6] if business_plan_data['contact_information'] is not None else ""
            phone = business_plan_data['contact_information'][7] if business_plan_data['contact_information'] is not None else ""
            email = business_plan_data['contact_information'][8] if business_plan_data['contact_information'] is not None else ""

            # financial table
            financing_sought = business_plan_data['financial'][2] if business_plan_data['financial'] is not None else ""
            profit_loss_statement = business_plan_data['financial'][3] if business_plan_data['financial'] is not None else ""
            break_even_analysis = business_plan_data['financial'][4] if business_plan_data['financial'] is not None else ""
            roi = business_plan_data['financial'][5] if business_plan_data['financial'] is not None else ""
            contingency_plan = business_plan_data['financial'][6] if business_plan_data['financial'] is not None else ""
            disaster_recovery_plan = business_plan_data['financial'][7] if business_plan_data['financial'] is not None else ""
            bank = business_plan_data['financial'][8] if business_plan_data['financial'] is not None else ""
            accounting_firm = business_plan_data['financial'][9] if business_plan_data['financial'] is not None else ""
            insurance_info = business_plan_data['financial'][10] if business_plan_data['financial'] is not None else ""

            # legal table
            intellectual_property = business_plan_data['legal'][2] if business_plan_data['legal'] is not None else ""
            law_firm = business_plan_data['legal'][3] if business_plan_data['legal'] is not None else ""

            self.initialize_edit_form(industry, employees, legal_structure, description, mission_statement, target_audience, principal_members, future,
                          products, services, pricing, research, industry_state, competitors,
                          company_advantages, regulations_compliance, growth_strategy, marketing_budget,
                          advertising_plan, customer_interaction, customer_retention, bank, accounting_firm,
                          financing_sought, profit_loss_statement, break_even_analysis, roi, contingency_plan,
                          disaster_recovery_plan, insurance_info, name, address, city, state, zip_code,
                          phone, email, law_firm, intellectual_property)
        else:
            self.initialize_create_form()

        # Initialize AI Chat section
        self.initialize_progress_tracker()
        self.initialize_ai_chat()

        # Create a frame to hold the buttons centered
        self.button_frame = CTkFrame(self.form_frame)
        self.button_frame.pack(side="top", pady=20)  # Adds padding at the top of the frame

        # Save Button
        self.submit_button = CTkButton(self.button_frame, text="Save", command=self.submit_business_plan)
        self.submit_button.pack(side="left", padx=10, pady=10)

        # Create PDF Button
        self.create_pdf_button = CTkButton(self.button_frame, text="Create PDF", command=self.create_pdf)
        self.create_pdf_button.pack(side="left", padx=10, pady=10)


    def help_explanation(self, message, event=None):
      CTkMessagebox(title="Explanation", message=message, icon="info")

    def create_label_and_help(self, text, row, column, help_text, help_explanation_func):
        """Create the label for the form field"""
        label = CTkLabel(self.scrollable_form_frame, text=text, font=("Arial", 14))
        label.grid(row=row, column=column, sticky="w", padx=(5, 10), pady=0)
        
        # Create the help icon and bind it to the explanation function
        help_icon_label = CTkLabel(self.scrollable_form_frame, text="", image=question_mark_ctk_image)
        help_icon_label.grid(row=row, column=column + 1, sticky="e", padx=(5, 10), pady=0)
        help_icon_label.bind("<Button-1>", lambda e: help_explanation_func(help_text))
        
        return label, help_icon_label

    def create_label(self, text, row, column):
        """Create the label for the form field"""
        label = CTkLabel(self.scrollable_form_frame, text=text, font=("Arial", 14))
        label.grid(row=row, column=column, sticky="w", padx=(5, 10), pady=0)
        
        return label
    
    def create_textbox(self, row, column, ht):
        """Create entry textbox for the form field"""
        entry = CTkTextbox(self.scrollable_form_frame, height=ht, wrap="word")
        entry.grid(row=row, column=column, padx=5, pady=5, sticky="ew", columnspan=2)
        
        return entry

    def edit_textbox(self, row, column, ht, default_value=None):
        """Create entry textbox for the form field and insert saved value"""
        # Create the textbox
        entry = CTkTextbox(self.scrollable_form_frame, height=ht, wrap="word")
        entry.grid(row=row, column=column, padx=5, pady=5, sticky="ew", columnspan=2)
        
        # Insert default value if provided
        if default_value:
            entry.insert("1.0", default_value)
        
        return entry

    def initialize_create_form(self):
        """Show form for creating a new business plan"""
        # Configure the column to expand
        self.scrollable_form_frame.grid_columnconfigure(0, weight=1)

        # General Info Section
        CTkLabel(self.scrollable_form_frame, text="General Information", font=("Arial", 17, "bold")).grid(row=0, column=0, sticky="w", padx=(5, 10), pady=(0,5))

        # Business name
        label, help_icon = self.create_label_and_help(
            text="Business Name:", 
            row=1, 
            column=0, 
            help_text="What would you like to call your business? Choose a name that reflects its purpose and stands out to your audience", 
            help_explanation_func=self.help_explanation
        )
        self.name_entry = self.create_textbox(row=2, column=0, ht=20)
        
        # Industry
        label, help_icon = self.create_label_and_help(
            text="Industry:", 
            row=3, 
            column=0, 
            help_text="What industry does your business belong to?", 
            help_explanation_func=self.help_explanation
        )
        self.industry_entry = self.create_textbox(row=4, column=0, ht=20)

        # Number of Employees
        label, help_icon = self.create_label_and_help(
            text="Number of Employees:", 
            row=5, 
            column=0, 
            help_text="The estimated number of employees your business will require.", 
            help_explanation_func=self.help_explanation
        )
        self.employees_entry = self.create_textbox(row=6, column=0, ht=20)

        # Legal Structure
        label, help_icon = self.create_label_and_help(
            text="Legal Structure:", 
            row=7, 
            column=0, 
            help_text="Is your business a sole proprietorship, partnership, LLC, etc.?", 
            help_explanation_func=self.help_explanation
        )
        self.legal_structure_entry = self.create_textbox(row=8, column=0, ht=20)

        # Executive Summary Section
        CTkLabel(self.scrollable_form_frame, text="Executive Summary", font=("Arial", 17, "bold")).grid(row=9, column=0, sticky="w", padx=(5, 10), pady=(10,5))

        # Description
        label, help_icon = self.create_label_and_help(
            text="Business Description:", 
            row=10, 
            column=0, 
            help_text="Describe your business. What products or services do you offer? What problem does your business solve, and how does it add value to customers?", 
            help_explanation_func=self.help_explanation
        )
        self.description_entry = self.create_textbox(row=11, column=0, ht=100)

        # Mission Statement
        label, help_icon = self.create_label_and_help(
            text="Mission Statement:", 
            row=12, 
            column=0, 
            help_text="What are the key objectives for your business? Think about both short-term and long-term goals that will help guide its growth and success.", 
            help_explanation_func=self.help_explanation
        )
        self.mission_statement_entry = self.create_textbox(row=13, column=0, ht=100)

        # Principal Business Members
        label, help_icon = self.create_label_and_help(
            text="Principal Members:", 
            row=14, 
            column=0, 
            help_text="Who are the key members of your business? Owners, management, board members, etc.", 
            help_explanation_func=self.help_explanation
        )
        self.principal_members_entry = self.create_textbox(row=15, column=0, ht=100)

        # Future of the company
        label, help_icon = self.create_label_and_help(
            text="Future Vision:", 
            row=16, 
            column=0, 
            help_text="Your vision for the future of the company. How you will fit into an ever-evolving world.", 
            help_explanation_func=self.help_explanation
        )
        self.future_entry = self.create_textbox(row=17, column=0, ht=100)

        # Products/Services Section
        CTkLabel(self.scrollable_form_frame, text="Products/Services", font=("Arial", 17, "bold")).grid(row=18, column=0, sticky="w", padx=(5, 10), pady=(10,5))

        # Products Offered
        label, help_icon = self.create_label_and_help(
            text="Products:", 
            row=19, 
            column=0, 
            help_text="What products does your company offer?", 
            help_explanation_func=self.help_explanation
        )
        self.products_entry = self.create_textbox(row=20, column=0, ht=100)

        # Services Offered
        label, help_icon = self.create_label_and_help(
            text="Services:", 
            row=21, 
            column=0, 
            help_text="What services does your company offer?", 
            help_explanation_func=self.help_explanation
        )
        self.services_entry = self.create_textbox(row=22, column=0, ht=100)

        # Pricing Structure
        label, help_icon = self.create_label_and_help(
            text="Pricing Structure:", 
            row=23, 
            column=0, 
            help_text="How are your products or services priced? Do you have a unique pricing model?", 
            help_explanation_func=self.help_explanation
        )
        self.pricing_entry = self.create_textbox(row=24, column=0, ht=100)

        # Research and Development
        label, help_icon = self.create_label_and_help(
            text="Research and Development:", 
            row=25, 
            column=0, 
            help_text="Do you have a need for research and development? What is your R&D plan if so? Costs, benefits?", 
            help_explanation_func=self.help_explanation
        )
        self.r_and_d_entry = self.create_textbox(row=26, column=0, ht=100)

        # Market Research Section
        CTkLabel(self.scrollable_form_frame, text="Market Research", font=("Arial", 17, "bold")).grid(row=27, column=0, sticky="w", padx=(5, 10), pady=(10,5))

        # State of the industry
        label, help_icon = self.create_label_and_help(
            text="Industry:", 
            row=28, 
            column=0, 
            help_text="What is the state of your industry? How will you fit in?", 
            help_explanation_func=self.help_explanation
        )
        self.industry_state_entry = self.create_textbox(row=29, column=0, ht=100)

        # Competitors
        label, help_icon = self.create_label_and_help(
            text="Competition:", 
            row=30, 
            column=0, 
            help_text="Who are your main competitors? What do they bring to the table?", 
            help_explanation_func=self.help_explanation
        )
        self.competitors_entry = self.create_textbox(row=31, column=0, ht=100)

        # Market Analysis
        CTkLabel(self.scrollable_form_frame, text="Market Analysis:", font=("Arial", 14)).grid(
            row=32, column=0, sticky="w", padx=(5, 10), pady=10
        )

        self.market_analysis_frame = CTkFrame(self.scrollable_form_frame)
        self.market_analysis_frame.grid(row=33, column=0, padx=5, pady=5, sticky="ew", columnspan=2)

        self.competitor_entries = []
        self.market_share_entries = []

        # Add initial row
        self.add_market_share_row()

        # Add competitor button
        CTkButton(
            self.scrollable_form_frame, text="Add Competitor", command=self.add_market_share_row
        ).grid(row=34, column=0, padx=5, pady=5, sticky="w")

        # Target audience
        label, help_icon = self.create_label_and_help(
            text="Target Audience:", 
            row=35, 
            column=0, 
            help_text="What is your target audience? Are they local, regional, worldwide?", 
            help_explanation_func=self.help_explanation
        )
        self.target_audience_entry = self.create_textbox(row=36, column=0, ht=100)

        # Company advantages
        label, help_icon = self.create_label_and_help(
            text="Company Advantages", 
            row=37, 
            column=0, 
            help_text="What advantage might you have over your competition? What do you bring to the table?", 
            help_explanation_func=self.help_explanation
        )
        self.advantages_entry = self.create_textbox(row=38, column=0, ht=100)

        # Regulations
        label, help_icon = self.create_label_and_help(
            text="Regulations & Compliance:", 
            row=39, 
            column=0, 
            help_text="Are there any industry-specific regulations you must adhere to? How do you plan to meet these standards?", 
            help_explanation_func=self.help_explanation
        )
        self.compliance_entry = self.create_textbox(row=40, column=0, ht=100)

        # Market Research Section
        CTkLabel(self.scrollable_form_frame, text="Marketing Strategy", font=("Arial", 17, "bold")).grid(row=41, column=0, sticky="w", padx=(5, 10), pady=(10,5))

        # Growth Strategy
        label, help_icon = self.create_label_and_help(
            text="Growth Strategy:", 
            row=42, 
            column=0, 
            help_text="Provide an overview of your growth strategy. How do you plan to expand, or do you plan to expand at all?", 
            help_explanation_func=self.help_explanation
        )
        self.growth_strategy_entry = self.create_textbox(row=43, column=0, ht=100)
        
        # Marketing Budget
        label, help_icon = self.create_label_and_help(
            text="Marketing Budget:", 
            row=44, 
            column=0, 
            help_text="What is your budget for marketing? Can it be broken down into muliple areas of spending? ", 
            help_explanation_func=self.help_explanation
        )
        self.marketing_budget_entry = self.create_textbox(row=45, column=0, ht=100)

        # Advertising Plan
        label, help_icon = self.create_label_and_help(
            text="Advertising:", 
            row=46, 
            column=0, 
            help_text="How do you plan to advertise? Television, online, word of mouth? Provide an overview of how you plan to let potential customers know about your business.", 
            help_explanation_func=self.help_explanation
        )
        self.adverising_entry = self.create_textbox(row=47, column=0, ht=100)

                # Customer Interaction
        label, help_icon = self.create_label_and_help(
            text="Customer Interaction:", 
            row=48, 
            column=0, 
            help_text="How do you plan to engage with your customer base? Social media, in-store, etc?", 
            help_explanation_func=self.help_explanation
        )
        self.interaction_entry = self.create_textbox(row=49, column=0, ht=100)

        # Retention
        label, help_icon = self.create_label_and_help(
            text="Customer Retention:", 
            row=50, 
            column=0, 
            help_text="How will you retain customers? Community outreach? Email lists?", 
            help_explanation_func=self.help_explanation
        )
        self.retention_entry = self.create_textbox(row=51, column=0, ht=100)

        # Financial Section
        CTkLabel(self.scrollable_form_frame, text="Financial Information", font=("Arial", 17, "bold")).grid(row=52, column=0, sticky="w", padx=(5, 10), pady=(10,5))

        # Bank
        label, help_icon = self.create_label_and_help(
            text="Bank:", 
            row=53, 
            column=0, 
            help_text="Which bank will you use for your business accounts?", 
            help_explanation_func=self.help_explanation
        )
        self.bank_entry = self.create_textbox(row=54, column=0, ht=100)

        # Accounting Firm
        label, help_icon = self.create_label_and_help(
            text="Accounting Firm:", 
            row=55, 
            column=0, 
            help_text="Which accounting firm or professional will you use?", 
            help_explanation_func=self.help_explanation
        )
        self.accounting_firm_entry = self.create_textbox(row=56, column=0, ht=100)

        # Financing Sought
        label, help_icon = self.create_label_and_help(
            text="Financing Sought:", 
            row=57, 
            column=0, 
            help_text="How much financing are you seeking? What are the terms?", 
            help_explanation_func=self.help_explanation
        )
        self.financing_entry = self.create_textbox(row=58, column=0, ht=100)

        # Profit/Loss Statement
        label, help_icon = self.create_label_and_help(
            text="Profit/Loss Statement:", 
            row=59, 
            column=0, 
            help_text="Summarize your business's revenue, expenses, and profits over a given period. This helps evaluate financial performance and guide decision-making.", 
            help_explanation_func=self.help_explanation
        )
        self.profit_loss_entry = self.create_textbox(row=60, column=0, ht=100)

        # Break Even Analysis
        label, help_icon = self.create_label_and_help(
            text="Break Even Analysis:", 
            row=61, 
            column=0, 
            help_text="Determine the point where your revenue matches your expenses, indicating when your business will start generating a profit.", 
            help_explanation_func=self.help_explanation
        )
        self.break_even_entry = self.create_textbox(row=62, column=0, ht=100)

        # Return on Investment (ROI)
        label, help_icon = self.create_label_and_help(
            text="Return on Investment (ROI):", 
            row=63, 
            column=0, 
            help_text="What ROI are you expecting, and how will you measure it? Within what timeframe are investors expecting to make a profit?", 
            help_explanation_func=self.help_explanation
        )
        self.roi_entry = self.create_textbox(row=64, column=0, ht=100)

        # Contingency Plan
        label, help_icon = self.create_label_and_help(
            text="Contingency Plan:", 
            row=65, 
            column=0, 
            help_text="What is your plan if things go wrong? Backup resources?", 
            help_explanation_func=self.help_explanation
        )
        self.contingency_entry = self.create_textbox(row=66, column=0, ht=100)

        # Disaster Recovery Plan
        label, help_icon = self.create_label_and_help(
            text="Disaster Recovery Plan:", 
            row=67, 
            column=0, 
            help_text="How will your business recover from disasters?", 
            help_explanation_func=self.help_explanation
        )
        self.disaster_recovery_entry = self.create_textbox(row=68, column=0, ht=100)

        # Insurance Information
        label, help_icon = self.create_label_and_help(
            text="Insurance Information:", 
            row=69, 
            column=0, 
            help_text="What insurance coverage does your business have or need?", 
            help_explanation_func=self.help_explanation
        )
        self.insurance_entry = self.create_textbox(row=70, column=0, ht=100)

        # Revenue Projection Section
        CTkLabel(self.scrollable_form_frame, text="Revenue Projection:", font=("Arial", 14)).grid(
            row=71, column=0, sticky="w", padx=(5, 10), pady=10
        )

        self.revenue_projection_frame = CTkFrame(self.scrollable_form_frame)
        self.revenue_projection_frame.grid(row=72, column=0, padx=5, pady=5, sticky="ew", columnspan=2)

        self.year_entries = []
        self.revenue_entries = []
        self.expenditure_entries = []

        # Add initial row
        self.add_revenue_row()

        # Add Year Button
        CTkButton(
            self.scrollable_form_frame, text="Add Year", command=self.add_revenue_row
        ).grid(row=73, column=0, padx=5, pady=5, sticky="w")

        # Legal Section
        CTkLabel(self.scrollable_form_frame, text="Legal Information", font=("Arial", 17, "bold")).grid(row=74, column=0, sticky="w", padx=(5, 10), pady=(10,5))

        # Law Firm
        label, help_icon = self.create_label_and_help(
            text="Law Firm:", 
            row=75, 
            column=0, 
            help_text="Which law firm or legal professional will handle your business's legal needs, such as contracts, compliance, or disputes?", 
            help_explanation_func=self.help_explanation
        )
        self.law_firm_entry = self.create_textbox(row=76, column=0, ht=100)

        # Intellectual Property
        label, help_icon = self.create_label_and_help(
            text="Intellectual Property:", 
            row=77, 
            column=0, 
            help_text="Detail any patents, trademarks, copyrights, or trade secrets that protect your business's products, services, or brand.", 
            help_explanation_func=self.help_explanation
        )
        self.intellectual_property_entry = self.create_textbox(row=78, column=0, ht=100)

        # Contact Info Section
        CTkLabel(self.scrollable_form_frame, text="Contact Information", font=("Arial", 17, "bold")).grid(row=79, column=0, sticky="w", padx=(5, 10), pady=(10,5))

        # Name
        label = self.create_label(text="Name:", row=80, column=0)
        self.contact_name_entry = self.create_textbox(row=81, column=0, ht=100)

        # Address
        label = self.create_label(text="Address:", row=82, column=0)
        self.address_entry = self.create_textbox(row=83, column=0, ht=100)

        # City
        label = self.create_label(text="City:", row=84, column=0)
        self.city_entry = self.create_textbox(row=85, column=0, ht=100)

        # State
        label = self.create_label(text="State:", row=86, column=0)
        self.state_entry = self.create_textbox(row=87, column=0, ht=100)

        # Zip
        label = self.create_label(text="Zip:", row=88, column=0)
        self.zip_entry = self.create_textbox(row=89, column=0, ht=100)

        # Phone
        label = self.create_label(text="Phone:", row=90, column=0)
        self.phone_entry = self.create_textbox(row=91, column=0, ht=100)

        # Email
        label = self.create_label(text="Email:", row=92, column=0)
        self.email_entry = self.create_textbox(row=93, column=0, ht=100)

     
        
    def initialize_edit_form(self, industry, employees, legal_structure, description, mission_statement, target_audience, principal_members, future,
                          products, services, pricing, research, industry_state, competitors,
                          company_advantages, regulations_compliance, growth_strategy, marketing_budget,
                          advertising_plan, customer_interaction, customer_retention, bank, accounting_firm,
                          financing_sought, profit_loss_statement, break_even_analysis, roi, contingency_plan,
                          disaster_recovery_plan, insurance_info, name, address, city, state, zip_code,
                          phone, email, law_firm, intellectual_property):
        
        """Show business plan form for editing a plan. Populate form fields with saved data."""
        # Configure the column to expand
        self.scrollable_form_frame.grid_columnconfigure(0, weight=1)

        # General Info Section
        CTkLabel(self.scrollable_form_frame, text="General Information", font=("Arial", 17, "bold")).grid(row=0, column=0, sticky="w", padx=(5, 10), pady=(0,5))

        # Business name
        """ CTkLabel(self.scrollable_form_frame, text="Business Name:", font=("Arial", 14)).grid(row=1, column=0, sticky="w", padx=(5, 10), pady=0)
        self.name_entry = CTkTextbox(self.scrollable_form_frame, height=20, wrap="word")
        self.name_entry.grid(row=2, column=0, padx=5, pady=5, sticky="ew", columnspan=2)
        self.name_entry.insert("1.0", self.original_business_name) """
        label, help_icon = self.create_label_and_help(
            text="Business Name:", 
            row=1, 
            column=0, 
            help_text="What would you like to call your business? Choose a name that reflects its purpose and stands out to your audience", 
            help_explanation_func=self.help_explanation
        )
        self.name_entry = self.edit_textbox(row=2, column=0, ht=20, default_value=self.original_business_name)

        # Industry
        label, help_icon = self.create_label_and_help(
            text="Industry:", 
            row=3, 
            column=0, 
            help_text="What industry does your business belong to?", 
            help_explanation_func=self.help_explanation
        )
        self.industry_entry = self.edit_textbox(row=4, column=0, ht=20, default_value=industry)

        # Number of Employees
        label, help_icon = self.create_label_and_help(
            text="Number of Employees:", 
            row=5, 
            column=0, 
            help_text="The estimated number of employees your business will require.", 
            help_explanation_func=self.help_explanation
        )
        self.employees_entry = self.edit_textbox(row=6, column=0, ht=20, default_value=employees)

        # Legal Structure
        label, help_icon = self.create_label_and_help(
            text="Legal Structure:", 
            row=7, 
            column=0, 
            help_text="Is your business a sole proprietorship, partnership, LLC, etc.?", 
            help_explanation_func=self.help_explanation
        )
        self.legal_structure_entry = self.edit_textbox(row=8, column=0, ht=20, default_value=legal_structure)

        # Executive Summary Section
        CTkLabel(self.scrollable_form_frame, text="Executive Summary", font=("Arial", 17, "bold")).grid(row=9, column=0, sticky="w", padx=(5, 10), pady=(10,5))

        # Description
        label, help_icon = self.create_label_and_help(
            text="Business Description:", 
            row=10, 
            column=0, 
            help_text="Describe your business. What products or services do you offer? What problem does your business solve, and how does it add value to customers?", 
            help_explanation_func=self.help_explanation
        )
        self.description_entry = self.edit_textbox(row=11, column=0, ht=100, default_value=description)

        # Mission Statement
        label, help_icon = self.create_label_and_help(
            text="Mission Statement:", 
            row=12, 
            column=0, 
            help_text="What are the key objectives for your business? Think about both short-term and long-term goals that will help guide its growth and success.", 
            help_explanation_func=self.help_explanation
        )
        self.mission_statement_entry = self.edit_textbox(row=13, column=0, ht=100, default_value=mission_statement)

        # Principal Business Members
        label, help_icon = self.create_label_and_help(
            text="Principal Members:", 
            row=14, 
            column=0, 
            help_text="Who are the key members of your business? Owners, management, board members, etc.", 
            help_explanation_func=self.help_explanation
        )
        self.principal_members_entry = self.edit_textbox(row=15, column=0, ht=100, default_value=principal_members)

        # Future of the company
        label, help_icon = self.create_label_and_help(
            text="Future Vision:", 
            row=16, 
            column=0, 
            help_text="Your vision for the future of the company. How you will fit into an ever-evolving world.", 
            help_explanation_func=self.help_explanation
        )
        self.future_entry = self.edit_textbox(row=17, column=0, ht=100, default_value=future)

        # Products/Services Section
        CTkLabel(self.scrollable_form_frame, text="Products/Services", font=("Arial", 17, "bold")).grid(row=18, column=0, sticky="w", padx=(5, 10), pady=(10,5))

        # Products Offered
        label, help_icon = self.create_label_and_help(
            text="Products:", 
            row=19, 
            column=0, 
            help_text="What products does your company offer?", 
            help_explanation_func=self.help_explanation
        )
        self.products_entry = self.edit_textbox(row=20, column=0, ht=100, default_value=products)

        # Services Offered
        label, help_icon = self.create_label_and_help(
            text="Services:", 
            row=21, 
            column=0, 
            help_text="What services does your company offer?", 
            help_explanation_func=self.help_explanation
        )
        self.services_entry = self.edit_textbox(row=22, column=0, ht=100, default_value=services)

        # Pricing Structure
        label, help_icon = self.create_label_and_help(
            text="Pricing Structure:", 
            row=23, 
            column=0, 
            help_text="How are your products or services priced? Do you have a unique pricing model?", 
            help_explanation_func=self.help_explanation
        )
        self.pricing_entry = self.edit_textbox(row=24, column=0, ht=100, default_value=pricing)

        # Research and Development
        label, help_icon = self.create_label_and_help(
            text="Research and Development:", 
            row=25, 
            column=0, 
            help_text="Do you have a need for research and development? What is your R&D plan if so? Costs, benefits?", 
            help_explanation_func=self.help_explanation
        )
        self.r_and_d_entry = self.edit_textbox(row=26, column=0, ht=100, default_value=research)

        # Market Research Section
        CTkLabel(self.scrollable_form_frame, text="Market Research", font=("Arial", 17, "bold")).grid(row=27, column=0, sticky="w", padx=(5, 10), pady=(10,5))

        # Industry Section
        label, help_icon = self.create_label_and_help(
            text="Industry:", 
            row=28, 
            column=0, 
            help_text="What is the state of your industry? How will you fit in?", 
            help_explanation_func=self.help_explanation
        )
        self.industry_state_entry = self.edit_textbox(row=29, column=0, ht=100, default_value=industry_state)

        # Competitors Section
        label, help_icon = self.create_label_and_help(
            text="Competition:", 
            row=30, 
            column=0, 
            help_text="Who are your main competitors? What do they bring to the table?", 
            help_explanation_func=self.help_explanation
        )
        self.competitors_entry = self.edit_textbox(row=31, column=0, ht=100, default_value=competitors)

        # Market Analysis
        CTkLabel(self.scrollable_form_frame, text="Market Analysis:", font=("Arial", 14)).grid(
            row=32, column=0, sticky="w", padx=(5, 10), pady=10
        )

        self.market_analysis_frame = CTkFrame(self.scrollable_form_frame)
        self.market_analysis_frame.grid(row=33, column=0, padx=5, pady=5, sticky="ew", columnspan=2)

        self.competitor_entries = []
        self.market_share_entries = []

        # Get existing market data
        market_data = get_market_share_projection(self.username, self.original_business_name)

        # Populate with existing market data
        for competitor, market_share in market_data:
            self.add_market_share_row(competitor=str(competitor), market_share=str(market_share))

        self.add_market_share_row()
        # Add competitor button
        CTkButton(
            self.scrollable_form_frame, text="Add Competitor", command=self.add_market_share_row
        ).grid(row=34, column=0, padx=5, pady=5, sticky="w")

        # Target Audience Section
        label, help_icon = self.create_label_and_help(
            text="Target Audience:", 
            row=35, 
            column=0, 
            help_text="What is your target audience? Are they local, regional, worldwide?", 
            help_explanation_func=self.help_explanation
        )
        self.target_audience_entry = self.edit_textbox(row=36, column=0, ht=100, default_value=target_audience)

        # Company Advantages Section
        label, help_icon = self.create_label_and_help(
            text="Company Advantages", 
            row=37, 
            column=0, 
            help_text="What advantage might you have over your competition? What do you bring to the table?", 
            help_explanation_func=self.help_explanation
        )
        self.advantages_entry = self.edit_textbox(row=38, column=0, ht=100, default_value=company_advantages)

        # Regulations Section
        label, help_icon = self.create_label_and_help(
            text="Regulations & Compliance:", 
            row=39, 
            column=0, 
            help_text="Are there any industry-specific regulations you must adhere to? How do you plan to meet these standards?", 
            help_explanation_func=self.help_explanation
        )
        self.compliance_entry = self.edit_textbox(row=40, column=0, ht=100, default_value=regulations_compliance)

        # Marketing Strategy Section
        CTkLabel(self.scrollable_form_frame, text="Marketing Strategy", font=("Arial", 17, "bold")).grid(row=41, column=0, sticky="w", padx=(5, 10), pady=(10,5))

        # Growth Strategy Section
        label, help_icon = self.create_label_and_help(
            text="Growth Strategy:", 
            row=42, 
            column=0, 
            help_text="Provide an overview of your growth strategy. How do you plan to expand, or do you plan to expand at all?", 
            help_explanation_func=self.help_explanation
        )
        self.growth_strategy_entry = self.edit_textbox(row=43, column=0, ht=100, default_value=growth_strategy)

        # Marketing Budget Section
        label, help_icon = self.create_label_and_help(
            text="Marketing Budget:", 
            row=44, 
            column=0, 
            help_text="What is your budget for marketing? Can it be broken down into multiple areas of spending?", 
            help_explanation_func=self.help_explanation
        )
        self.marketing_budget_entry = self.edit_textbox(row=45, column=0, ht=100, default_value=marketing_budget)

        # Advertising Plan Section
        label, help_icon = self.create_label_and_help(
            text="Advertising:", 
            row=46, 
            column=0, 
            help_text="How do you plan to advertise? Television, online, word of mouth? Provide an overview of how you plan to let potential customers know about your business.", 
            help_explanation_func=self.help_explanation
        )
        self.adverising_entry = self.edit_textbox(row=47, column=0, ht=100, default_value=advertising_plan)

        # Customer Interaction Section
        label, help_icon = self.create_label_and_help(
            text="Customer Interaction:", 
            row=48, 
            column=0, 
            help_text="How do you plan to engage with your customer base? Social media, in-store, etc?", 
            help_explanation_func=self.help_explanation
        )
        self.interaction_entry = self.edit_textbox(row=49, column=0, ht=100, default_value=customer_interaction)

        # Retention Section
        label, help_icon = self.create_label_and_help(
            text="Customer Retention:", 
            row=50, 
            column=0, 
            help_text="How will you retain customers? Community outreach? Email lists?", 
            help_explanation_func=self.help_explanation
        )
        self.retention_entry = self.edit_textbox(row=51, column=0, ht=100, default_value=customer_retention)

        # Financial Information Section
        CTkLabel(self.scrollable_form_frame, text="Financial Information", font=("Arial", 17, "bold")).grid(row=52, column=0, sticky="w", padx=(5, 10), pady=(10,5))

        # Bank Section
        label, help_icon = self.create_label_and_help(
            text="Bank:", 
            row=53, 
            column=0, 
            help_text="Which bank will you use for your business accounts?", 
            help_explanation_func=self.help_explanation
        )
        self.bank_entry = self.edit_textbox(row=54, column=0, ht=100, default_value=bank)

        # Accounting Firm Section
        label, help_icon = self.create_label_and_help(
            text="Accounting Firm:", 
            row=55, 
            column=0, 
            help_text="Which accounting firm or professional will you use?", 
            help_explanation_func=self.help_explanation
        )
        self.accounting_firm_entry = self.edit_textbox(row=56, column=0, ht=100, default_value=accounting_firm)

        # Financing Sought Section
        label, help_icon = self.create_label_and_help(
            text="Financing Sought:", 
            row=57, 
            column=0, 
            help_text="How much financing are you seeking? What are the terms?", 
            help_explanation_func=self.help_explanation
        )
        self.financing_entry = self.edit_textbox(row=58, column=0, ht=100, default_value=financing_sought)

        # Profit/Loss Statement Section
        label, help_icon = self.create_label_and_help(
            text="Profit/Loss Statement:", 
            row=59, 
            column=0, 
            help_text="Summarize your business's revenue, expenses, and profits over a given period. This helps evaluate financial performance and guide decision-making.", 
            help_explanation_func=self.help_explanation
        )
        self.profit_loss_entry = self.edit_textbox(row=60, column=0, ht=100, default_value=profit_loss_statement)

        # Break Even Analysis Section
        label, help_icon = self.create_label_and_help(
            text="Break Even Analysis:", 
            row=61, 
            column=0, 
            help_text="Determine the point where your revenue matches your expenses, indicating when your business will start generating a profit.", 
            help_explanation_func=self.help_explanation
        )
        self.break_even_entry = self.edit_textbox(row=62, column=0, ht=100, default_value=break_even_analysis)

        # Return on Investment (ROI) Section
        label, help_icon = self.create_label_and_help(
            text="Return on Investment (ROI):", 
            row=63, 
            column=0, 
            help_text="What ROI are you expecting, and how will you measure it? Within what timeframe are investors expecting to make a profit?", 
            help_explanation_func=self.help_explanation
        )
        self.roi_entry = self.edit_textbox(row=64, column=0, ht=100, default_value=roi)

        # Contingency Plan Section
        label, help_icon = self.create_label_and_help(
            text="Contingency Plan:", 
            row=65, 
            column=0, 
            help_text="What is your plan if things go wrong? Backup resources?", 
            help_explanation_func=self.help_explanation
        )
        self.contingency_entry = self.edit_textbox(row=66, column=0, ht=100, default_value=contingency_plan)

        # Disaster Recovery Plan Section
        label, help_icon = self.create_label_and_help(
            text="Disaster Recovery Plan:", 
            row=67, 
            column=0, 
            help_text="How will your business recover from disasters?", 
            help_explanation_func=self.help_explanation
        )
        self.disaster_recovery_entry = self.edit_textbox(row=68, column=0, ht=100, default_value=disaster_recovery_plan)

        # Insurance Information Section
        label, help_icon = self.create_label_and_help(
            text="Insurance Information:", 
            row=69, 
            column=0, 
            help_text="What insurance coverage does your business have or need?", 
            help_explanation_func=self.help_explanation
        )
        self.insurance_entry = self.edit_textbox(row=70, column=0, ht=100, default_value=insurance_info)

        # Revenue Projection
        CTkLabel(self.scrollable_form_frame, text="Revenue Projection:", font=("Arial", 14)).grid(
            row=71, column=0, sticky="w", padx=(5, 10), pady=10
        )

        self.revenue_projection_frame = CTkFrame(self.scrollable_form_frame)
        self.revenue_projection_frame.grid(row=72, column=0, padx=5, pady=5, sticky="ew", columnspan=2)

        self.year_entries = []
        self.revenue_entries = []
        self.expenditure_entries = []

        # Fetch existing revenue projections from the database
        revenue_data = get_revenue_projection(self.username, self.original_business_name)

        # Populate rows with existing data from the database
        for year, revenue, expenditure in revenue_data:
            self.add_revenue_row(year=str(year), revenue=str(revenue), expenditure=str(expenditure))

        self.add_revenue_row()
        # Add Year Button
        CTkButton(
            self.scrollable_form_frame, text="Add Year", command=self.add_revenue_row
        ).grid(row=73, column=0, padx=5, pady=5, sticky="w")

        # Legal Section
        CTkLabel(self.scrollable_form_frame, text="Legal Information", font=("Arial", 17, "bold")).grid(row=74, column=0, sticky="w", padx=(5, 10), pady=(10,5))

        # Law Firm
        label, help_icon = self.create_label_and_help(
            text="Law Firm:", 
            row=75, 
            column=0, 
            help_text="Which law firm or legal professional will handle your business's legal needs, such as contracts, compliance, or disputes?", 
            help_explanation_func=self.help_explanation
        )
        self.law_firm_entry = self.edit_textbox(row=76, column=0, ht=100, default_value=law_firm)

        # Intellectual Property
        label, help_icon = self.create_label_and_help(
            text="Intellectual Property:", 
            row=77, 
            column=0, 
            help_text="Detail any patents, trademarks, copyrights, or trade secrets that protect your business's products, services, or brand.", 
            help_explanation_func=self.help_explanation
        )
        self.intellectual_property_entry = self.edit_textbox(row=78, column=0, ht=100, default_value=intellectual_property)

        # Contact Info Section
        CTkLabel(self.scrollable_form_frame, text="Contact Information", font=("Arial", 17, "bold")).grid(row=79, column=0, sticky="w", padx=(5, 10), pady=(10,5))

        # Name
        label = self.create_label(text="Name:", row=80, column=0)
        self.contact_name_entry = self.edit_textbox(row=81, column=0, ht=100, default_value=name)

        # Address
        label = self.create_label(text="Address:", row=82, column=0)
        self.address_entry = self.edit_textbox(row=83, column=0, ht=100, default_value=address)

        # City
        label = self.create_label(text="City:", row=84, column=0)
        self.city_entry = self.edit_textbox(row=85, column=0, ht=100, default_value=city)

        # State
        label = self.create_label(text="State:", row=86, column=0)
        self.state_entry = self.edit_textbox(row=87, column=0, ht=100, default_value=state)

        # Zip
        label = self.create_label(text="Zip:", row=88, column=0)
        self.zip_entry = self.edit_textbox(row=89, column=0, ht=100, default_value=zip_code)

        # Phone
        label = self.create_label(text="Phone:", row=90, column=0)
        self.phone_entry = self.edit_textbox(row=91, column=0, ht=100, default_value=phone)

        # Email
        label = self.create_label(text="Email:", row=92, column=0)
        self.email_entry = self.edit_textbox(row=93, column=0, ht=100, default_value=email)


    def add_revenue_row(self, year="", revenue="", expenditure=""):
        """Add a row for entering year and revenue data"""
        row_frame = CTkFrame(self.revenue_projection_frame)
        row_frame.pack(fill="x", pady=5)

        year_entry = CTkEntry(row_frame, placeholder_text="Year", width=150)
        year_entry.pack(side="left", padx=10)
        if year:
            year_entry.insert(0, year)
        self.year_entries.append(year_entry)

        revenue_entry = CTkEntry(row_frame, placeholder_text="Revenue", width=150)
        revenue_entry.pack(side="left", padx=0)
        if revenue:
            revenue_entry.insert(0, revenue)
        self.revenue_entries.append(revenue_entry)

        expenditure_entry = CTkEntry(row_frame, placeholder_text="Expenditure", width=150)
        expenditure_entry.pack(side="left", padx=10)
        if expenditure:
            expenditure_entry.insert(0, expenditure)
        self.expenditure_entries.append(expenditure_entry)

    def add_market_share_row(self, competitor="", market_share=""):
        """Add a row for entering competitor and market share data"""
        row_frame = CTkFrame(self.market_analysis_frame)
        row_frame.pack(fill="x", pady=5)

        # Competitor entry
        competitor_entry = CTkEntry(row_frame, placeholder_text="Competitor Name", width=250)
        competitor_entry.pack(side="left", padx=5)
        if competitor:
            competitor_entry.insert(0, competitor)
        self.competitor_entries.append(competitor_entry)

        # Market share entry
        market_share_entry = CTkEntry(row_frame, placeholder_text="Market Share (%)", width=150)
        market_share_entry.pack(side="left", padx=5)
        if market_share:
            market_share_entry.insert(0, market_share)
        self.market_share_entries.append(market_share_entry)

    def initialize_progress_tracker(self):
        # Circular Progressbar
        self.progress_bar = awesometkinter.RadialProgressbar(
            self.progress_tracker_frame, fg='red', parent_bg="#2a2d2e", size=(80, 80)  
        )
        self.progress_bar.pack(side="left", padx=(165,0), pady=10)

        self.progress_label = CTkLabel(self.progress_tracker_frame, text="Progress", font=("Arial", 12))
        self.progress_label.pack(side="right", padx=(0,120),pady=5)
        
        # Initialize progress tracking
        self.total_fields = len(self.collect_fields())
        self.completed_fields = 0
        self.update_progress_bar()
    
    
    def initialize_ai_chat(self):
        """Initialize the AI Chat section in ai_frame"""
        
        # Chat box
        self.chat_box = CTkTextbox(self.ai_frame, width=380, height=400, state='disabled')
        self.chat_box.pack(pady=10, fill="y")

        # User input
        self.user_input = CTkEntry(self.ai_frame, width=380)
        self.user_input.pack(pady=10)
        self.user_input.bind("<Return>", self.send_message)

        # Create a frame to hold the buttons centered
        self.ai_button_frame = CTkFrame(self.ai_frame)
        self.ai_button_frame.pack(side="top", pady=20)  # Adds padding at the bottom of the frame

        # Send button
        self.send_button = CTkButton(self.ai_button_frame, text="Send", command=self.send_message)
        self.send_button.pack(padx=10, pady=10)

    def update_progress_bar(self):
            """Update the circular progress bar."""
            completion_percentage = self.calculate_completion()
            self.progress_bar.set(completion_percentage)  # Set the percentage
            self.progress_label.configure(text=f"Progress: {int(completion_percentage)}%")
    
    def submit_business_plan(self):
        """Submit the business plan. Either initially or as an update."""
        

        self.update_progress_bar()
        """Submit the business plan. Either initially or as an update."""
        # Collect data from form fields
        new_business_name = self.name_entry.get("1.0", "end").strip()
        industry = self.industry_entry.get("1.0", "end").strip()
        employees = self.employees_entry.get("1.0", "end").strip()
        legal_structure = self.legal_structure_entry.get("1.0", "end").strip()
        percentage = self.calculate_completion()

        # Executive Summary
        description = self.description_entry.get("1.0", "end").strip()
        mission_statement = self.mission_statement_entry.get("1.0", "end").strip()
        principal_members = self.principal_members_entry.get("1.0", "end").strip()
        future = self.future_entry.get("1.0", "end").strip()
        
        # Products/services
        products = self.products_entry.get("1.0", "end").strip()
        services = self.services_entry.get("1.0", "end").strip()
        pricing = self.pricing_entry.get("1.0", "end").strip()
        research = self.r_and_d_entry.get("1.0", "end").strip()

        # Market Research
        industry_state = self.industry_state_entry.get("1.0", "end").strip()
        competitors = self.competitors_entry.get("1.0", "end").strip()
        target_audience = self.target_audience_entry.get("1.0", "end").strip()
        company_advantages = self.advantages_entry.get("1.0", "end").strip()
        regulations_compliance = self.compliance_entry.get("1.0", "end").strip()

        # Marketing Strategy Section
        growth_strategy = self.growth_strategy_entry.get("1.0", "end").strip() 
        marketing_budget = self.marketing_budget_entry.get("1.0", "end").strip()
        advertising_plan = self.adverising_entry.get("1.0", "end").strip()
        customer_interaction = self.interaction_entry.get("1.0", "end").strip()
        customer_retention = self.retention_entry.get("1.0", "end").strip()

        # Financial Section
        bank = self.bank_entry.get("1.0", "end").strip()
        accounting_firm = self.accounting_firm_entry.get("1.0", "end").strip()
        financing_sought = self.financing_entry.get("1.0", "end").strip()
        profit_loss_statement = self.profit_loss_entry.get("1.0", "end").strip()
        break_even_analysis = self.break_even_entry.get("1.0", "end").strip()
        roi = self.roi_entry.get("1.0", "end").strip()
        contingency_plan = self.contingency_entry.get("1.0", "end").strip()
        disaster_recovery_plan = self.disaster_recovery_entry.get("1.0", "end").strip()
        insurance_info = self.insurance_entry.get("1.0", "end").strip()

        # Contact Info
        name = self.contact_name_entry.get("1.0", "end").strip()  # Reusing the same name entry (or can be a new one)
        address = self.address_entry.get("1.0", "end").strip()
        city = self.city_entry.get("1.0", "end").strip()
        state = self.state_entry.get("1.0", "end").strip()
        zip_code = self.zip_entry.get("1.0", "end").strip()
        phone = self.phone_entry.get("1.0", "end").strip()
        email = self.email_entry.get("1.0", "end").strip()

        # Legal Information
        law_firm = self.law_firm_entry.get("1.0", "end").strip()
        intellectual_property = self.intellectual_property_entry.get("1.0", "end").strip()


        # Collect revenue projection data
        years = [entry.get().strip() for entry in self.year_entries if entry.get().strip().isdigit()]
        revenues = [entry.get().strip() for entry in self.revenue_entries if entry.get().strip().isdigit()]
        expenditures = [entry.get().strip() for entry in self.expenditure_entries if entry.get().strip().isdigit()]

        if len(years) != len(revenues) or len(years) != len(expenditures):
            CTkMessagebox(title="Error", message="Please enter valid year, revenue, and expenditure data!", icon="error")
            return

        revenue_projection = [{"year": int(year), "revenue": int(revenue), "expenditure": int(expenditure)} for year, revenue, expenditure in zip(years, revenues, expenditures)]

        # Collect market share data
        main_competitors = [entry.get().strip() for entry in self.competitor_entries if entry.get().strip()]
        market_shares = [entry.get().strip() for entry in self.market_share_entries if entry.get().strip().isdigit()]

        if len(main_competitors) != len(market_shares):
            CTkMessagebox(title="Error", message="Please enter valid competitor names and market shares!", icon="error")
            return

        market_analysis = [{"competitor": competitor, "market_share": int(market_share)} for competitor, market_share in zip(main_competitors, market_shares)]
        

        # Combine all data for submission
        data = {
            "username": self.username,
            "business_name": new_business_name,
            "employees":employees,
            "legal_structure":legal_structure,
            "industry":industry,
            "percentage":percentage,

            # Executive summary
            "description": description,
            "mission_statement": mission_statement,
            "principal_members": principal_members,
            "future": future,
            
            # Products/Services Section
            "products": products,
            "services": services,
            "pricing": pricing,
            "research": research,
            
            # Market Research Section
            "industry_state": industry_state,
            "competitors":competitors,
            "target_audience": target_audience,
            "company_advantages": company_advantages,
            "regulations_compliance": regulations_compliance,
            
            # Marketing Strategy Section
            "growth_strategy": growth_strategy,
            "marketing_budget": marketing_budget,
            "advertising_plan": advertising_plan,
            "customer_interaction": customer_interaction,
            "customer_retention": customer_retention,
            
            # Financial Section
            "bank": bank,
            "accounting_firm": accounting_firm,
            "financing_sought": financing_sought,
            "profit_loss_statement": profit_loss_statement,
            "break_even_analysis": break_even_analysis,
            "roi": roi,
            "contingency_plan": contingency_plan,
            "disaster_recovery_plan": disaster_recovery_plan,
            "insurance_info": insurance_info,
            
            # Contact Info Section
            "contact_name": name,
            "address": address,
            "city": city,
            "state": state,
            "zip_code": zip_code,
            "phone": phone,
            "email": email,

            #Legal
            "law_firm":law_firm,
            "intellectual_property":intellectual_property,

            # Revenue projection
            "revenue_projection":revenue_projection,

            # Market shares
            "market_analysis":market_analysis
        }
        if self.original_business_name:
        # Update existing business plan
            if new_business_name != self.original_business_name:
                if check_business_name_exists(new_business_name):
                    print(f"Business name '{new_business_name}' already exists. Choose a different name.")
                    return
            print(f"Industry: {industry}")
            print(f"Description: {description}")
            update_business_plan(self.original_business_name, data)
            print("Business Plan Updated in Database")
        else:
            # Create new business plan
            insert_business_plan(self.username, data)
            print("Business Plan Submitted and Saved to Database")

        self.master.load_business_plans()
        self.close_window()
    
    def close_window(self):
        ''' Close the current business plan window'''
        if self in self.master.open_windows:
            self.master.open_windows.remove(self)
        self.destroy()
    
    def collect_fields(self):
        """Collect all form fields to calculate progress."""
        return [
            self.name_entry, self.industry_entry, self.employees_entry, self.legal_structure_entry,
            self.description_entry, self.mission_statement_entry, self.principal_members_entry, self.future_entry,
            self.products_entry, self.services_entry, self.pricing_entry, self.r_and_d_entry,
            self.industry_state_entry, self.competitors_entry, self.target_audience_entry, self.advantages_entry,
            self.compliance_entry, self.growth_strategy_entry, self.marketing_budget_entry, self.adverising_entry,
            self.interaction_entry, self.retention_entry, self.bank_entry, self.accounting_firm_entry,
            self.financing_entry, self.profit_loss_entry, self.break_even_entry, self.roi_entry,
            self.contingency_entry, self.disaster_recovery_entry, self.insurance_entry, self.contact_name_entry,
            self.address_entry, self.city_entry, self.state_entry, self.zip_entry, self.phone_entry,
            self.email_entry, self.law_firm_entry, self.intellectual_property_entry
        ]

    def calculate_completion(self):
        """Calculate the completion percentage based on filled fields."""
        filled_fields = sum(
            bool(field.get("1.0", "end").strip()) for field in self.collect_fields()
        )
        return (filled_fields / self.total_fields) * 100


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

def bind_field_updates(self):
    """Bind <KeyRelease> to update progress as user fills the form fields."""
    for field in self.collect_fields():
        field.bind("<KeyRelease>", lambda e: self.update_progress_bar())

        
