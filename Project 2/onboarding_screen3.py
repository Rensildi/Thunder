import customtkinter as ctk
from pathlib import Path
from PIL import Image
from database import resource_path

ASSETS_PATH = Path(resource_path("images\frame2"))


#def relative_to_assets(path: str) -> Path:
    #return ASSETS_PATH / Path(path)


def run(parent_window, on_next):
    frame = ctk.CTkFrame(parent_window, fg_color="#105090")
    frame.pack(fill="both", expand=True)

    label_title = ctk.CTkLabel(frame, text="Get Started!", font=("JacquesFrancois Regular", 40), text_color="#FFFDFD")
    label_title.place(x=334, y=73)

    label_description = ctk.CTkLabel(
        frame,
        text="You're ready to start building your business with Thunder.\nPress ‘Get Started’ to access your dashboard and begin creating!",
        font=("JacquesFrancois Regular", 20),
        text_color="#FFFDFD",
    )
    label_description.place(x=143, y=163)

    #image_path = relative_to_assets("image_1.png")
    pil_image = Image.open(resource_path("images/image_3_1.png"))
    image = ctk.CTkImage(light_image=pil_image, size=(200, 200))
    label_image = ctk.CTkLabel(frame, image=image, text="")
    label_image.place(x=350, y=260)

    button_exit = ctk.CTkButton(
        frame,
        text="Get Started",
        command=lambda: [frame.destroy(), on_next()],
        fg_color="#331B59",
        hover_color="#FFC300",
        text_color="white",
        font=("JacquesFrancois Regular", 18),
        width=124,
        height=42,
    )
    button_exit.place(x=387, y=492)
