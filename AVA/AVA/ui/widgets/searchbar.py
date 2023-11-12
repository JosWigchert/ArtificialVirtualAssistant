import customtkinter as ctk


class TextBar(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.entry = ctk.CTkEntry(self)
        self.entry.pack(side="left", padx=5)
        self.button = ctk.CTkButton(self, text="Search", command=self.search)
        self.button.pack(side="right", padx=5)

    def search(event=None):
        query = search_entry.get()
        # Perform your search or other action here
        print(f"Searching for: {query}")


root = ctk.CTk()
root.title("Search Bar Example")

# Create a frame for the search bar
search_frame = ctk.CTkFrame(root)
search_frame.pack(pady=10)

# Create a text field
search_entry = ctk.CTkEntry(search_frame, width=300)
search_entry.pack(side="left", padx=5)

# Create a search button
search_button = ctk.CTkButton(search_frame, text="Search", command=search)
search_button.pack(side="right", padx=5)

# Bind the Enter key to the search function
search_entry.bind("<Return>", search)

root.mainloop()
