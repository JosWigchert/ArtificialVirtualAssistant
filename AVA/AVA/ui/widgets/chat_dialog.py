import customtkinter as ctk
import tkinter as tk
import threading


class ChatBubble(ctk.CTkFrame):
    def __init__(
        self, master, user: str, message: str, is_user: bool = True, *args, **kwargs
    ):
        super().__init__(master, *args, **kwargs)

        master.bind("<Configure>", self.update_wraplength, add="+")

        self.user = user
        self.message = message
        self.corner_radius = 20
        self._corner_radius = self.corner_radius
        self.user_frame = ctk.CTkFrame(self, corner_radius=self.corner_radius)
        self.message_frame = ctk.CTkFrame(self, corner_radius=self.corner_radius)

        if is_user:
            self.sticky = "e"
        else:
            self.sticky = "w"

        self.user_label = ctk.CTkLabel(
            self.user_frame,
            text=self.user,
            font=("Calibri", 14, "bold"),
            anchor=self.sticky,
            justify="left",
            corner_radius=self.corner_radius,
        )
        self.message_label = ctk.CTkLabel(
            self.message_frame,
            text=self.message,
            font=("Calibri", 18),
            anchor=self.sticky,
            justify="left",
            corner_radius=self.corner_radius,
        )

        self.user_label.pack(fill="both", expand=True)
        self.message_label.pack(fill="both", expand=True)

        self.user_frame.grid(
            row=0, column=0, sticky=self.sticky, padx=(0, 0), pady=(0, 0)
        )
        self.message_frame.grid(
            row=1, column=0, sticky=self.sticky, padx=(0, 0), pady=(5, 0)
        )

    def update_wraplength(self, event):
        wraplength = int(0.8 * event.width)
        self.message_label.configure(wraplength=wraplength)

    def update_text(self, text):
        self.message = text
        self.message_label.configure(text=self.message)


class ChatDialog(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master=master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.chat_bubbles: list[ChatBubble] = []
        self.lock = threading.Lock()
        self.place(relwidth=1, relheight=1)

        # self.add_bubble(False, "John", "Hello!")
        # self.add_bubble(True, "Jane", "Hi John, how are you?")

    def add_bubble(self, is_user: bool, user: str, message: str):
        bubble = ChatBubble(master=self, is_user=is_user, user=user, message=message)
        bubble.grid(sticky=bubble.sticky, column=0, columnspan=2)
        self.chat_bubbles.append(bubble)

    def message_callback(self, index, old, new):
        if old is None and new is not None:
            # append
            with self.lock:
                self.add_bubble(
                    new["is_user"], "User" if new["is_user"] else "AVA", new["content"]
                )
            pass
        if old is not None and new is not None:
            # update
            with self.lock:
                self.chat_bubbles[index].update_text(new["content"])
            pass
        if old is not None and new is None:
            # delete
            pass


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CustomTkinter complex_example.py")
        self.geometry(f"{600}x{800}")

        self.my_frame = ChatDialog(master=self, width=600, height=800)


if __name__ == "__main__":
    app = App()
    app.mainloop()
