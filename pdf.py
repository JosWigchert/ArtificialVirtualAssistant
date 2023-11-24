<<<<<<< HEAD
import customtkinter as ctk
import tkinter as tk
import fitz
from threading import Thread
from AVA.ui.widgets import PDFViewer


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("950x900")

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

    def continue_words(self):
        next_words = []
        words = self.pdf_document.load_page(self.current_page).get_text("words")
        if self.last_word == words[-1]:
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
                return ""
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
=======
try:
    from tkinter import *
    import fitz
    from tkinter.ttk import Progressbar
    from threading import Thread
    import math
except Exception as e:
    print(f"This error occured while importing neccesary modules or library {e}")


class ShowPdf:
    img_object_li = []

    def pdf_view(
        self, master, width=1200, height=600, pdf_location="", bar=True, load="after"
    ):
        self.frame = Frame(master, width=width, height=height, bg="white")

        scroll_y = Scrollbar(self.frame, orient="vertical")
        scroll_x = Scrollbar(self.frame, orient="horizontal")

        scroll_x.pack(fill="x", side="bottom")
        scroll_y.pack(fill="y", side="right")

        percentage_view = 0
        percentage_load = StringVar()

        if bar == True and load == "after":
            self.display_msg = Label(textvariable=percentage_load)
            self.display_msg.pack(pady=10)

            loading = Progressbar(
                self.frame, orient=HORIZONTAL, length=100, mode="determinate"
            )
            loading.pack(side=TOP, fill=X)

        self.text = Text(
            self.frame,
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            width=width,
            height=height,
        )
        self.text.pack(side="left")

        scroll_x.config(command=self.text.xview)
        scroll_y.config(command=self.text.yview)

        def add_img():
            precentage_dicide = 0
            open_pdf = fitz.open(pdf_location)

            for page in open_pdf:
                pix = page.getPixmap()
                pix1 = fitz.Pixmap(pix, 0) if pix.alpha else pix
                img = pix1.getImageData("ppm")
                timg = PhotoImage(data=img)
                self.img_object_li.append(timg)
                if bar == True and load == "after":
                    precentage_dicide = precentage_dicide + 1
                    percentage_view = (
                        float(precentage_dicide) / float(len(open_pdf)) * float(100)
                    )
                    loading["value"] = percentage_view
                    percentage_load.set(
                        f"Please wait!, your pdf is loading {int(math.floor(percentage_view))}%"
                    )
            if bar == True and load == "after":
                loading.pack_forget()
                self.display_msg.pack_forget()

            for i in self.img_object_li:
                self.text.image_create(END, image=i)
                self.text.insert(END, "\n\n")
            self.text.configure(state="disabled")

        def start_pack():
            t1 = Thread(target=add_img)
            t1.start()

        if load == "after":
            master.after(250, start_pack)
        else:
            start_pack()

        return self.frame


def main():
    root = Tk()
    root.geometry("700x780")
    d = ShowPdf().pdf_view(
        root,
        pdf_location="/home/jos/Documents/Obsidian/MasterProjectDocumentation/Literature Review/Papers/BANA.pdf",
        width=50,
        height=200,
    )
    d.pack()
    root.mainloop()


if __name__ == "__main__":
    main()
>>>>>>> 1a04da6 (Add tts)
