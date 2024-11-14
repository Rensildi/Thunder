from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage
import os

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\rkala\OneDrive\Desktop\Thunder\Project 2\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def exit_program():
    window.destroy()


window = Tk()
window.geometry("900x600")
window.configure(bg="#105090")

canvas = Canvas(window, bg="#105090", height=600, width=900, bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=0, y=0)
canvas.create_rectangle(359.0, 481.0, 543.0, 546.0, fill="#105090", outline="")

button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(image=button_image_1, borderwidth=0, highlightthickness=0, command=exit_program, relief="flat")
button_1.place(x=387.0, y=492.0, width=124.0, height=42.0)

canvas.create_text(334.0, 73.0, anchor="nw", text="Get Started!", fill="#FFFDFD", font=("JacquesFrancois Regular", 40 * -1))
canvas.create_text(143.0, 163.0, anchor="nw", text="You're ready to start building your business with Thunder.\nPress ‘Get Started’ to access your dashboard and begin creating!", fill="#FFFFFF", font=("JacquesFrancois Regular", 20 * -1))

image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
canvas.create_image(450.0, 353.0, image=image_image_1)

window.resizable(False, False)
window.mainloop()