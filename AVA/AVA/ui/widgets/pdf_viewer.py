import customtkinter as ctk
import fitz
from PIL import Image
from threading import Thread
import math
from AVA.events import Event
from AVA.ui.widgets.scrollable_frame import ScrollableFrame


class PDFViewer(ctk.CTkFrame):
    def __init__(
        self,
        master,
        bar: bool = True,
        **kwargs,
    ):
        super().__init__(master, **kwargs)

        self.bar = bar
        self.loaded = Event()

        self.percentage_load = ctk.StringVar()
        if bar == True:
            self.display_msg = ctk.CTkLabel(self, textvariable=self.percentage_load)
            self.loading = ctk.CTkProgressBar(
                self, orientation=ctk.HORIZONTAL, mode="determinate"
            )
            self.loading.set(0)

        self.pages_frame = ctk.CTkScrollableFrame(self)  # , vscroll=True, hscroll=True)
        self.pages_frame.pack(fill="both", expand=True)
        self.pages = []

    def load(self, pdf_document: fitz.Document):
        t1 = Thread(target=self._load, args=(pdf_document,))
        t1.start()

    def _unload(self):
        for page in self.pages:
            page.pack_forget()
            page.destroy()

        self.pages = []

    def _load(self, pdf_document: fitz.Document):
        self._unload()

        self.display_msg.pack(pady=10)
        self.loading.pack(side=ctk.TOP, fill=ctk.X)

        precentage_dicide = 0
        self.pdf_document = pdf_document
        for i, page in enumerate(self.pdf_document):
            mat = fitz.Matrix(1.5, 1.5)
            pix = page.get_pixmap(matrix=mat)

            if len(self.pages) > 0:
                self.configure(width=pix.width)
                self.pages_frame.configure(width=pix.width)

            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            photo = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
            print(f"size of page {i} = {[pix.width, pix.height]}, {img.size}")

            # Create a Label with the image and pack it into the scrollable frame
            label = ctk.CTkLabel(self.pages_frame, image=photo, text="")
            label.pack(padx=10, pady=10)

            self.pages.append(label)

            if self.bar == True:
                precentage_dicide = precentage_dicide + 1
                percentage_view = float(precentage_dicide) / float(
                    len(self.pdf_document)
                )
                self.loading.set(percentage_view)
                self.percentage_load.set(
                    f"Please wait!, your pdf is loading {int(percentage_view * 100)}%"
                )

        if self.bar == True:
            self.loading.pack_forget()
            self.display_msg.pack_forget()

        self.loaded.publish()


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("700x780")
        pdf_location = (
            r"D:\Data\Jos\MasterProjectDocumentation\Literature Review\Papers\BANA.pdf"
        )
        self.pdf_document = fitz.open(pdf_location)
        self.pdf_viewer = PDFViewer(master=self)
        self.pdf_viewer.pack(fill=ctk.BOTH, expand=True)
        self.pdf_viewer.load(self.pdf_document)


if __name__ == "__main__":
    app = App()
    app.mainloop()
