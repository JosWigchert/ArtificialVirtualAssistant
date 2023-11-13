import tkinter as tk
import customtkinter as ctk
from PIL import Image

from AVA.ui.widgets import *
from AVA.ui.assets import assetManager
import os


ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"


class ChatbotGui(ctk.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Chatbot")
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
        self.top_bar.grid(
            row=0,
            column=0,
            columnspan=2,
            # padx=self.default_pad,
            # pady=self.default_pad,
            sticky="ew",
        )
        self.top_bar.configure(height=40)

        self.title_label = ctk.CTkLabel(
            self.top_bar, text="AVA", font=("Calibri", 18, "bold")
        )
        self.title_label.pack(
            padx=self.default_pad, pady=self.default_pad, side=tk.LEFT
        )

        self.search_bar = TextBar(
            self.top_bar, assetManager.get("search"), height=self.top_bar["height"]
        )
        self.search_bar.pack(
            side=tk.TOP, fill=tk.X, padx=self.default_pad, pady=self.default_pad
        )

    def init_chat(self):
        self.chat = ChatFrame(self, corner_radius=0)
        self.chat.grid(row=1, column=1, columnspan=4, sticky="nsew")

        self.chat_input = TextBar(self, assetManager.get("send"), height=40)
        self.chat_input.grid(row=2, column=1, sticky="ew")

    def init_side_panel(self):
        self.side_panel = ctk.CTkFrame(self, corner_radius=0)
        self.side_panel.grid(
            row=1,
            column=0,
            rowspan=2,
            # padx=self.default_pad,
            # pady=self.default_pad,
            sticky="nsew",
        )
        self.side_panel.configure(width=40)

        # --------------------------------------------- #
        self.add_button = ctk.CTkButton(
            self.side_panel,
            image=assetManager.get("add"),
            text="",
        )
        self.add_button.configure(
            width=self.side_panel["width"], height=self.side_panel["width"]
        )
        self.add_button.pack(
            padx=self.default_pad, pady=self.default_pad, ipadx=0, ipady=0
        )
        # --------------------------------------------- #


if __name__ == "__main__":
    app = ChatbotGui()
    app.mainloop()
