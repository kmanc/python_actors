import abc
import queue
import time
from py_actors.control import DoneMessage, FlushMessage
from py_actors.log_config import actor_logger


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

    def on_shutdown(self):
        actor_logger.info(f'{self.name} was shut down')

    @staticmethod
    def call(actor):
        while actor.is_running:
            if actor.is_complete:
                break
            try:
                message = actor.message_queue.get_nowait()
                actor.on_receive(message)
            except queue.Empty:
                time.sleep(.25)
        actor.on_shutdown()
        return actor.is_complete

    def post(self, message):
        try:
            assert self.is_running is True and self.is_complete is False
            return self.message_queue.put_nowait(message)
        except queue.Full:
            actor_logger.error(f'The queue for {self.name} is full, shutting down')
            self.shutdown()
        except AssertionError:
            actor_logger.error(f'A message was sent to {self.name} after it stopped running or was marked as complete')
            self.shutdown()

    def do_lookup(self, name):
        return self.actor_lookup[name]

    def shutdown(self):
        self.is_running = False


class BatchJoinActor(Actor):

    def __init__(self, key_list):
        super().__init__()
        self.key_list = key_list
        self.num_done = 0
        self.results = []

    def on_receive(self, message):
        if type(message) == DoneMessage:
            self.num_done += 1
            if self.num_done >= len(self.key_list):
                self.is_complete = True
        else:
            self.results.extend(message)


class BatchSplitActor(Actor):

    def __init__(self, key_list, batch_size=256):
        super().__init__()
        self.key_list = key_list
        self.batch_size = batch_size
        self.batch_dict = dict(zip(key_list, [[] for i in range(len(key_list))]))

    def on_receive(self, message):
        if type(message) == DoneMessage:
            for key in self.key_list:
                instance = self.do_lookup(key)
                final_batch = self.batch_dict[key]
                if final_batch:
                    instance.post(final_batch)
                instance.post(DoneMessage())
            self.is_complete = True
        elif type(message) == FlushMessage:
            for key in self.key_list:
                instance = self.do_lookup(key)
                flush_batch = self.batch_dict[key]
                if flush_batch:
                    actor_logger.debug(f'Flushing {flush_batch}')
                    instance.post(flush_batch)
                self.batch_dict[key] = []
        else:
            try:
                message_iterable = iter(message)
                while True:
                    for key in self.key_list:
                        self.batch_dict[key].append(next(message_iterable))
                        if len(self.batch_dict[key]) >= self.batch_size:
                            instance = self.do_lookup(key)
                            instance.post(self.batch_dict[key])
                            self.batch_dict[key] = []
            except StopIteration:
                pass
            except TypeError:
                actor_logger.error(f'{self.name} was given a non-iterable message')
                self.shutdown()


class CountdownActor(Actor):

    def __init__(self, count):
        super().__init__()
        self.count = count

    def on_receive(self, message):
        self.do_work(message)
        self.count -= 1
        if self.count <= 0:
            self.is_complete = True

    @classmethod
    def do_work(cls, message):
        pass


class JoinActor(Actor):

    def __init__(self, key_list):
        super().__init__()
        self.key_list = key_list
        self.num_done = 0
        self.results = []

    def on_receive(self, message):
        if type(message) == DoneMessage:
            self.num_done += 1
            if self.num_done >= len(self.key_list):
                self.is_complete = True
        else:
            self.results.append(message)


class SplitActor(Actor):

    def __init__(self, key_list):
        super().__init__()
        self.key_list = key_list

    def on_receive(self, message):
        if type(message) == DoneMessage:
            for needs_shutdown in self.key_list:
                shut_me_down = self.do_lookup(needs_shutdown)
                shut_me_down.post(DoneMessage())
            self.is_complete = True
        else:
            try:
                message_iterable = iter(message)
                while True:
                    for key in self.key_list:
                        instance = self.do_lookup(key)
                        instance.post(next(message_iterable))
            except StopIteration:
                pass
            except TypeError:
                actor_logger.error(f'{self.name} was given a non-iterable message')
                self.shutdown()



