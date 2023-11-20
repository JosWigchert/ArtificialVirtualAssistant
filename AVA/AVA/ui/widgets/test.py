import customtkinter as ctk
from AVA.events import Event
from AVA.ui.assets import assetManager


class TextBar(ctk.CTkFrame):
    def __init__(self, master, button_asset, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        message = "this is a test"
        self.event = Event()
        self.entry = ctk.CTkLabel(self, height=self["height"], text=message)
        self.entry.pack(side=ctk.LEFT, expand=True, padx=(0, 5), fill=ctk.X)

        message += "another text"
        self.entry.configure(text=message)

    def search(self):
        self.event.publish(text=self.entry.get())


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("TextBar Demo")
        self.geometry(f"{600}x{800}")

        self.bar = TextBar(
            master=self, button_asset=assetManager.get("send"), width=800, height=40
        )
        self.bar.pack(pady=10, fill=ctk.X, side=ctk.TOP, padx=10)


if __name__ == "__main__":
    app = App()
    app.mainloop()
