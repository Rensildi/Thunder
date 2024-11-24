import customtkinter as ctk
from pathlib import Path
from PIL import Image
from database import resource_path

#ASSETS_PATH = Path(resource_path("images\frame0"))


#def relative_to_assets(path: str) -> Path:
    #return ASSETS_PATH / Path(path)


def run(parent_window, on_next):
    """Run the first tutorial screen"""
    frame = ctk.CTkFrame(parent_window, fg_color="#105090")
    frame.pack(fill="both", expand=True)

    label_title = ctk.CTkLabel(
        frame, text="Welcome to Thunder!", font=("JacquesFrancois Regular", 40), text_color="#FFFDFD"
    )
    label_title.place(x=242, y=51)

    label_description = ctk.CTkLabel(
        frame,
        text="We're excited to help you turn your ideas into actionable business plans.\nThunder is designed to be intuitive and user-friendly.",
        font=("JacquesFrancois Regular", 16),
        text_color="#FFFDFD",
    )
    label_description.place(x=208, y=380)

    #image_path = relative_to_assets("image_1.png")
    pil_image = Image.open(resource_path("images/image_1.png"))
    image = ctk.CTkImage(light_image=pil_image, size=(200, 200))
    label_image = ctk.CTkLabel(frame, image=image, text="")
    label_image.place(x=349, y=105)
    
    button_next = ctk.CTkButton(
        frame,
        text="Next",
        command=lambda: [frame.destroy(), on_next()],
        fg_color="#331B59",
        hover_color="#FFC300",
        text_color="white",
        font=("JacquesFrancois Regular", 18),
        width=195,
        height=54,
    )
    button_next.place(x=352, y=492)
