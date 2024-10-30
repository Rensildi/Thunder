from customtkinter import *
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

class ChatApp(CTk):
    def __init__(self):
        super().__init__()
        self.title("llama bro")
        self.geometry("400x500")
        
        self.context = ""
        
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
    
    def send_message(self, event=None):
        user_message = self.user_input.get()
        
        # Close convo
        if user_message.lower() == "exit":
            self.quit()
        
        self.chat_box.configure(state='normal')
        self.chat_box.insert('end', f"You: {user_message}\n")
        self.chat_box.configure(state='disabled')
        self.chat_box.yview('end') # Scroll to the bottom
        
        self.user_input.delete(0,'end')
        
        # Generate response from llama bro
        result = chain.invoke({"context": self.context, "question": user_message})
        self.context += f"\nUser: {user_message}\nLlama: {result}"
        
        # llama bro response
        self.chat_box.configure(state='normal')
        self.chat_box.insert('end', f"llama: {result}\n")
        self.chat_box.configure(state='disabled')
        self.chat_box.yview('end')
        
if __name__ == "__main__":
    app = ChatApp()
    app.mainloop()




