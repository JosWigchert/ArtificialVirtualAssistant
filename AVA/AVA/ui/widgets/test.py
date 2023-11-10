import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageDraw


def create_rounded_mask(width, height, corner_radius):
    mask = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(mask)

    draw.rectangle((0, 0, width, height), fill=255)
    draw.pieslice((0, 0, corner_radius * 2, corner_radius * 2), 180, 270, fill=0)
    draw.pieslice(
        (width - 2 * corner_radius, 0, width, corner_radius * 2), 270, 360, fill=0
    )
    mask = mask.resize((width, height))
    return mask


# Example usage:
if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("400x200")

    corner_radius = 20

    label1 = ctk.CTkLabel(root, text="Top Rounded Label")
    label1.grid(pady=5, padx=10, sticky="w", row=0, column=0)

    mask1 = create_rounded_mask(
        label1.winfo_width(), label1.winfo_height(), corner_radius
    )
    label1.photo = tk.PhotoImage(mask=mask1)
    label1.config(image=label1.photo)

    label2 = ctk.CTkLabel(root, text="Another Label")
    label2.grid(pady=5, padx=10, sticky="s", row=1, column=0)

    mask2 = create_rounded_mask(
        label2.winfo_width(), label2.winfo_height(), corner_radius
    )
    label2.photo = ctk.CTkPhotoImage(mask=mask2)
    label2.config(image=label2.photo)

    root.mainloop()
