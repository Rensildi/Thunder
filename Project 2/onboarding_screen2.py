import customtkinter as ctk
from pathlib import Path
from PIL import Image

ASSETS_PATH = Path(r"C:\Users\rkala\OneDrive\Desktop\Thunder\Project 2\images\frame1")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def run(parent_window, on_next):
    frame = ctk.CTkFrame(parent_window, fg_color="#105090")
    frame.pack(fill="both", expand=True)

    label_title = ctk.CTkLabel(frame, text="Flexibility", font=("JacquesFrancois Regular", 40), text_color="#FFFDFD")
    label_title.place(x=354, y=73)

    label_description = ctk.CTkLabel(
        frame,
        text="Structure, refine, and visualize your business plan with ease.",
        font=("JacquesFrancois Regular", 30),
        text_color="#FFFDFD",
    )
    label_description.place(x=42, y=186)

    image1_path = relative_to_assets("image_1.png")
    pil_image1 = Image.open(image1_path)
    image1 = ctk.CTkImage(light_image=pil_image1, size=(200, 200))
    label_image1 = ctk.CTkLabel(frame, image=image1, text="")
    label_image1.place(x=200, y=260)

    image2_path = relative_to_assets("image_2.png")
    pil_image2 = Image.open(image2_path)
    image2 = ctk.CTkImage(light_image=pil_image2, size=(200, 200))
    label_image2 = ctk.CTkLabel(frame, image=image2, text="")
    label_image2.place(x=540, y=260)

    button_next = ctk.CTkButton(
        frame,
        text="Next",
        command=lambda: [frame.destroy(), on_next()],
        fg_color="#331B59",
        hover_color="#FFC300",
        text_color="white",
        font=("JacquesFrancois Regular", 18),
        width=124,
        height=42,
    )
    button_next.place(x=555, y=499)

    button_exit = ctk.CTkButton(
        frame,
        text="Exit",
        command=lambda: [frame.destroy(), parent_window.destroy()],
        fg_color="#331B59",
        hover_color="#CC0000",
        text_color="white",
        font=("JacquesFrancois Regular", 18),
        width=124,
        height=42,
    )
    button_exit.place(x=244, y=502)
