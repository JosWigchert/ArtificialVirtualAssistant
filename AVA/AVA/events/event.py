import threading


class Event:
    def __init__(self):
        self.handlers = []

    def subscribe(self, handler):
        if callable(handler):
            self.handlers.append(handler)

    def unsubscribe(self, handler):
        if handler in self.handlers:
            self.handlers.remove(handler)

    def publish(self, *args, **kwargs):
        for handler in self.handlers:
            if callable(handler):
                t = threading.Thread(target=handler, args=args, kwargs=kwargs)
                t.start()
