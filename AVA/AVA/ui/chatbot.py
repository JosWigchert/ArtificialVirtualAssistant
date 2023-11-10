import tkinter as tk
import customtkinter as ctk
from PIL import Image

from AVA.ui.widgets import *
import os

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("CustomTkinter complex_example.py")
        self.geometry(f"{800}x{600}")

        self.default_pad = 5

        self.grid_columnconfigure(0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0)
        self.grid_rowconfigure(1, weight=1)

        self.init_top_bar()
        self.init_chat()
        self.init_side_panel()

    def init_top_bar(self):
        self.top_bar = ctk.CTkFrame(self, corner_radius=0)
        self.top_bar.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.top_bar.configure(height=50)

        self.title_label = ctk.CTkLabel(
            self.top_bar, text="Chatbot", font=("Calibri", 18, "bold")
        )
        self.title_label.pack(
            padx=self.default_pad, pady=self.default_pad, side=tk.LEFT
        )

    def init_chat(self):
        self.chat = ChatFrame(self)
        self.chat.grid(row=1, column=1, rowspan=4, columnspan=4, sticky="nsew")

    def init_side_panel(self):
        self.side_panel = ctk.CTkFrame(self, corner_radius=0)
        self.side_panel.grid(row=1, column=0, rowspan=2, sticky="nsew")
        self.side_panel.configure(width=40)

        # --------------------------------------------- #
        self.add_button = ctk.CTkButton(
            self.side_panel,
            image=ctk.CTkImage(
                light_image=Image.open("AVA\\AVA\\ui\\assets\\add.png".replace("/", os.sep).replace("\\", os.sep)),
                dark_image=Image.open("AVA\\AVA\\ui\\assets\\add.png".replace("/", os.sep).replace("\\", os.sep)),
            ),
            text="",
        )
        self.add_button.configure(
            width=self.side_panel["width"], height=self.side_panel["width"]
        )
        self.add_button.pack(
            padx=self.default_pad, pady=self.default_pad, ipadx=0, ipady=0
        )
        # --------------------------------------------- #

    def open_side_panel(self):
        self.side_panel.animate()


if __name__ == "__main__":
    app = App()
    app.mainloop()
