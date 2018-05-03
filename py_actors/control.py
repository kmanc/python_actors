from threading import Lock


class CallbackFuture:

    def __init__(self):
        self.results = None
        self.lock = Lock()
        self.lock.acquire()

    def callback(self, data):
        try:
            self.results = data
        finally:
            self.lock.release()

    def done(self):
        with self.lock:
            return self.results


class DoneMessage:
    pass


class FlushMessage:
    pass
