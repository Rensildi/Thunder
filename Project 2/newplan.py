from customtkinter import CTkToplevel, CTkLabel, CTkEntry, CTkButton, CTkTextbox
from database import insert_business_plan, update_business_plan, check_business_name_exists
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

template = """
Answer the question below.

Here is the conversation history: {context}

Question: {question}

Answer: 
"""

model = OllamaLLM(model="llama3")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

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
        self.chat_box.yview('end') # Scroll to the bottom
        
        self.user_input.delete(0,'end')
        
        # Generate response from llama bro
        result = chain.invoke({"context": self.context, "question": user_message})
        self.context += f"\nUser: {user_message}\nLlama: {result}"
        
        # llama bro response
        self.chat_box.configure(state='normal')
        self.chat_box.insert('end', f"llama: {result}\n\n")
        self.chat_box.configure(state='disabled')
        self.chat_box.yview('end')

