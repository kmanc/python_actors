import multiprocessing


class MicroKernelConfig(object):

    def __init__(self):
        self.MAX_THREADS = max(64, multiprocessing.cpu_count() * 4)
        self.ACTOR_MESSAGE_QUEUE_SIZE = 64

    def set_max_threads(self, number):
        self.MAX_THREADS = number

    def set_actor_message_queue_size(self, size):
        self.ACTOR_MESSAGE_QUEUE_SIZE = size
