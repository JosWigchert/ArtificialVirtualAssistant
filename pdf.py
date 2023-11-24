import customtkinter as ctk
import tkinter as tk
import fitz
from threading import Thread
from AVA.ui.widgets import PDFViewer
from AVA.model import OpenAI
from AVA.utils import Environment


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("950x900")

        self.env = Environment()
        self.openai = OpenAI(
            self.env.OPENAI_API_KEY,
            self.env.OPENAI_ENGINE,
            self.env.OPENAI_EMBEDDINGS,
            stream=True,
        )

        # Menu Bar
        menu_bar = tk.Menu(self)
        m1 = tk.Menu(menu_bar, tearoff=0)
        m1.add_command(label="Open File", command=self.open_file)
        m1.add_separator()
        m1.add_command(label="Save File", command=lambda: self.save_final(0))
        self.config(menu=menu_bar)

        menu_bar.add_cascade(label="File", menu=m1)
        m2 = tk.Menu(menu_bar, tearoff=0)
        m2.add_command(label="Light theme", command=lambda: self.theme_selection(0))
        m2.add_command(label="Dark theme", command=lambda: self.theme_selection(1))
        m2.add_separator()
        m2.add_command(label="System theme", command=lambda: self.theme_selection(2))
        self.config(menu=menu_bar)
        menu_bar.add_cascade(label="Setting", menu=m2)

        m3 = tk.Menu(menu_bar, tearoff=0)
        m3.add_command(label="help!", command=lambda: self.help_us())

        self.config(menu=menu_bar)
        menu_bar.add_cascade(label="Help", menu=m3)

        # PDF
        self.pdf_viewer = PDFViewer(master=self)
        self.pdf_viewer.pack(fill=ctk.BOTH, expand=True)
        self.pdf_viewer.loaded.subscribe(self.on_pdf_viewer_loaded)

        self.continue_button = ctk.CTkButton(
            self, text="Continue", command=self.continue_button_pressed
        )
        self.continue_button.pack(side=ctk.BOTTOM, pady=10)

        self.pdf_document = None
        self.current_page = 0
        self.last_word = None

        self.audio = Audio()

    def theme_selection(self, theme):
        if theme == 0:
            ctk.set_appearance_mode("light")
        elif theme == 1:
            ctk.set_appearance_mode("dark")
        elif theme == 2:
            ctk.set_appearance_mode("system")

    def help_us(self):
        print("help")

    def open_file(self):
        file_location = ctk.filedialog.askopenfilename(
            initialdir=r"D:\Data\Jos\MasterProjectDocumentation\Literature Review\Papers",
            title="Select file",
            filetypes=(("PDF files", "*.pdf"), ("all files", "*.*")),
        )
        if file_location:
            self.pdf_document = fitz.open(file_location)
            self.pdf_viewer.load(self.pdf_document)

    def exit_program(self):
        self.quit()
        self.destroy()

    def on_pdf_viewer_loaded(self):
        self.words = []
        for i, page in enumerate(self.pdf_viewer.pages):
            page.bind("<Button-1>", lambda event, i=i: self.click(event, i))

    def continue_button_pressed(self):
        self.continue_words()

    def click(self, event, page_number):
        x, y = event.x, event.y

        x = x / 1.5
        y = y / 1.5
        words = self.pdf_document.load_page(page_number).get_text("words")

        print(f"Text at position ({x}, {y}) on page {page_number}: ")

        next_words = []
        self.current_page = page_number
        self.last_word = None
        for word in words:
            if word[0] <= x <= word[2] and word[1] <= y <= word[3]:
                next_words.append(word[4])
                self.last_word = word
            elif len(next_words) > 0 and len(next_words) <= 100:
                if next_words[-1].endswith("-"):
                    next_words[-1] = next_words[-1][:-1] + word[4]
                    self.last_word = word
                else:
                    next_words.append(word[4])
                    self.last_word = word
        words = " ".join(next_words)
        print(words)

        if len(next_words) > 0:
            audio = self.openai.generate_tts(words)
            self.audio.play(audio)

    def continue_words(self):
        if not self.pdf_document:
            return

        next_words = []
        words = self.pdf_document.load_page(self.current_page).get_text("words")
        if not self.last_word:
            for word in words:
                if len(next_words) <= 100:
                    if len(next_words) > 0 and next_words[-1].endswith("-"):
                        next_words[-1] = next_words[-1][:-1] + word[4]
                        self.last_word = word
                    else:
                        next_words.append(word[4])
                        self.last_word = word
                else:
                    break
        elif self.last_word == words[-1]:
            if self.current_page < len(self.pdf_viewer.pages) - 1:
                self.current_page = self.current_page + 1
                words = self.pdf_document.load_page(self.current_page).get_text("words")
                for word in words:
                    if len(next_words) <= 100:
                        if len(next_words) > 0 and next_words[-1].endswith("-"):
                            next_words[-1] = next_words[-1][:-1] + word[4]
                            self.last_word = word
                        else:
                            next_words.append(word[4])
                            self.last_word = word
                    else:
                        break
        else:
            add_next = False
            for word in words:
                if add_next and len(next_words) <= 100:
                    if len(next_words) > 0 and next_words[-1].endswith("-"):
                        next_words[-1] = next_words[-1][:-1] + word[4]
                        self.last_word = word
                    else:
                        next_words.append(word[4])
                        self.last_word = word
                elif word == self.last_word:
                    add_next = True
        words = " ".join(next_words)
        print(words)


if __name__ == "__main__":
    app = App()
    app.mainloop()
