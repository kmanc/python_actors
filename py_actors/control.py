from threading import Lock


class CallbackFuture:

    def __init__(self):
        self.results = None
        self.mu = Lock()
        self.mu.acquire()

    def callback(self, data):
        try:
            self.results = data
        finally:
            self.mu.release()

    def done(self):
        try:
            self.mu.acquire()
            return self.results
        finally:
            self.mu.release()


class DoneMessage:
    pass


class FlushMessage:
    pass
