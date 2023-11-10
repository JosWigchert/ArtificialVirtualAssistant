from AVA.ui.loading.loadingThread import LoadingThread
import time


class HandleMessageThread(LoadingThread):
    def __init__(self, message: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.message = message

    def run(self):
        time.sleep(5)
