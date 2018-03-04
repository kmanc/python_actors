import abc
import concurrent.futures
import micro_kernel_config
import queue


class Actor(concurrent.futures.Future):

    def __init__(self):
        self.config = micro_kernel_config.MicroKernelConfig()

        self.is_running = True
        self.is_complete = False
        self.message_queue = queue.Queue()
        self.actor_lookup = dict()

    @abc.abstractclassmethod
    def on_receive(self, message):
        pass

    @abc.abstractclassmethod
    def get_name(self):
        pass

    def on_init(self):
        pass

    def on_complete(self):
        pass

    def on_shutdown(self):
        pass

    #@Override
    def call(self):
        while self.is_running and not self.is_complete:
            try:
                message = self.message_queue.get_nowait()
            except queue.Empty:
                message = None
            if message:
                size = self.message_queue.qsize()
                half = self.config.ACTOR_MESSAGE_QUEUE_SIZE >> 1
                if size == 0:
                    self.on_receive(message)
                elif size > half:
                    array = list()
                    for i in range(half):
                        array.append(self.message_queue.get_nowait())
                    for stored_message in array:
                        self.on_receive(stored_message)
        return

    def post(self, message):
        try:
            return self.message_queue.put_nowait(message)
        except queue.Full:
            print('I dont know what to do but the queue is full')

    def do_lookup(self, name):
        return self.actor_lookup[name]

    def shutdown(self):
        self.is_running = False
        self.on_shutdown()

    def set_complete(self):
        self.is_complete = True
