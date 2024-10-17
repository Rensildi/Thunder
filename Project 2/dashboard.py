from customtkinter import*

class Dashboard(CTk):
    def __init__(self, username):
        super().__init__()
        
        self.geometry("600x400")
        self.title(f"{username}'s dashboard")
        
        # Dashboard Label
        self.label = CTkLabel(self, text="Welcome to the Dashboard!", font=("Arial", 24))
        self.label.pack(pady=20)
        
if __name__=="__main__":
    app = Dashboard(username="TestUser")
    app.mainloop()