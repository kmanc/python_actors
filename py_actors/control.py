from threading import Lock


class CallbackFuture:
    """A future that can be used to return the result(s) of an actor's work"""

    def __init__(self):
        self.results = None
        self.lock = Lock()
        self.lock.acquire()

    def callback(self, data):
        """Callback that receives the data from an actor. Should be called in the actor's on_complete method"""
        try:
            self.results = data
        finally:
            self.lock.release()

    def done(self):
        """Method for extracting data from the callback. Should be called in the 'main' code function"""
        with self.lock:
            return self.results


class DoneMessage:
    """Message type indicating to an actor that it is done processing work"""
    pass


class FlushMessage:
    """Message type indicating to a batch actor that it should flush all current batches"""
    pass
