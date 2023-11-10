from AVA.ui.loading.loadingThread import LoadingThread
from AVA.database import PineconeDatabase


class InitializeDatabaseThread(LoadingThread):
    def __init__(self, db: PineconeDatabase, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = db

    def run(self):
        print("Initializing database...")
        self.db.initialize()
        print("Database initialized!")
