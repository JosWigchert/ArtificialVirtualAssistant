import customtkinter as ctk
from random import choice


class SidePanel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent)

        self._corner_radius = 0
        # general attributes
        self.collapsed_pos = -200
        self.expanded_pos = 0
        self.width = abs(
            self.collapsed_pos - self.expanded_pos
        )  # Set the fixed width here

        # animation logic
        self.pos = self.collapsed_pos
        self.collapsed = True
        self.ismoving = False

        # layout
        self.place(x=self.collapsed_pos, relheight=1, relwidth=1)
        self.configure(width=self.width)

    def animate(self):
        if self.ismoving:
            return

        if self.collapsed:
            self.animate_expand()
        else:
            self.animate_collapse()

    def animate_expand(self):
        self.ismoving = True
        if self.pos < self.expanded_pos:
            self.pos += 1 * 3
            self.place(x=self.pos)
            self.after(1, self.animate_expand)
        else:
            self.ismoving = False
            self.collapsed = False

    def animate_collapse(self):
        self.ismoving = True
        if self.pos > self.collapsed_pos:
            self.pos -= 1
            self.place(x=self.pos)
            self.after(1, self.animate_collapse)
        else:
            self.ismoving = False
            self.collapsed = True


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Animated Widgets")
        self.geometry(f"{600}x{800}")

        # animated widget
        animated_panel = SidePanel(self)
        ctk.CTkLabel(animated_panel, text="Label 1").pack(expand=True, padx=2, pady=10)
        ctk.CTkLabel(animated_panel, text="Label 2").pack(expand=True, padx=2, pady=10)
        ctk.CTkButton(animated_panel, text="Button", corner_radius=0).pack(expand=True)
        ctk.CTkTextbox(animated_panel, fg_color=("#dbdbdb", "#2b2b2b")).pack(
            expand=True
        )

        # button
        self.button_x = 0.5
        self.button = ctk.CTkButton(
            self, text="toggle sidebar", command=animated_panel.animate
        )
        self.button.place(relx=self.button_x, rely=0.5, anchor="center")


if __name__ == "__main__":
    app = App()
    app.mainloop()
