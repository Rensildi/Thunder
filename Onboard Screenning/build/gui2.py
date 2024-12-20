
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\rkala\OneDrive\Desktop\Thunder\Onboard Screenning\build\assets\frame2")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("900x600")
window.configure(bg = "#105090")


canvas = Canvas(
    window,
    bg = "#105090",
    height = 600,
    width = 900,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_text(
    242.0,
    51.0,
    anchor="nw",
    text="Welcome to Thunder!",
    fill="#FFFDFD",
    font=("JacquesFrancois Regular", 40 * -1)
)

canvas.create_text(
    208.0,
    380.0,
    anchor="nw",
    text="We're excited to help you turn your ideas into actionable business plans. \nThunder is designed to be intuitive, user friendly, and efficient your all in one\n toolkit for bringing your vision to life.",
    fill="#FFFDFD",
    font=("JacquesFrancois Regular", 16 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=352.0,
    y=492.0,
    width=195.0,
    height=54.0
)

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    449.0,
    251.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    538.0,
    185.0,
    image=image_image_2
)
window.resizable(False, False)
window.mainloop()
