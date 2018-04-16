import abc
import queue
from log_config import actor_logger


class Actor(abc.ABC):

    def __init__(self):
        self.actor_lookup = None
        self.is_running = True
        self.is_complete = False
        self.message_queue = queue.Queue()
        self.name = None

    @classmethod
    def on_receive(cls, message):
        pass

    def get_name(self):
        return self.name

    def on_init(self, lookup):
        self.actor_lookup = lookup

    def on_complete(self):
        actor_logger.info(f'{self.name} has finished')
        pass

    def on_shutdown(self):
        actor_logger.info(f'{self.name} was shut down')
        pass

    @staticmethod
    def call(actor):
        while actor.is_running:
            if actor.is_complete:
                break
            try:
                message = actor.message_queue.get_nowait()
                actor.on_receive(message)
            except queue.Empty:
                pass
        actor.on_shutdown()
        return actor.is_complete

    def post(self, message):
        try:
            assert self.is_running is True and self.is_complete is False
            return self.message_queue.put_nowait(message)
        except queue.Full:
            actor_logger.error(f'The queue for {self.name} is full, exiting')
            exit(0)
        except AssertionError:
            actor_logger.error(f'A message {self.name} after it was completed')
            exit(0)

    def do_lookup(self, name):
        return self.actor_lookup[name]

    def shutdown(self):
        self.is_running = False


class DoneMessage:
    pass


class FlushMessage:
    pass
