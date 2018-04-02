import abc
import queue


class Actor(abc.ABC):

    def __init__(self):
        self.actor_lookup = None

        self.is_running = True
        self.is_complete = False
        self.message_queue = queue.Queue()

    @abc.abstractclassmethod
    def on_receive(self, message):
        pass

    @abc.abstractclassmethod
    def get_name(self):
        pass

    def on_init(self, lookup):
        self.actor_lookup = lookup

    def on_complete(self):
        pass

    def on_shutdown(self):
        pass

    @staticmethod
    def call(actor):
        while actor.is_running and not actor.is_complete:
            try:
                message = actor.message_queue.get_nowait()
                actor.on_receive(message)
            except queue.Empty:
                pass
        actor.is_complete = True
        return True

    def post(self, message):
        try:
            return self.message_queue.put_nowait(message)
        except queue.Full:
            print('The queue is full')
            exit(0)

    def do_lookup(self, name):
        return self.actor_lookup[name]

    def shutdown(self):
        self.is_running = False
        self.on_shutdown()
