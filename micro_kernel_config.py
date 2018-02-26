import multiprocessing


class MicroKernelConfig(object):

    def __init__(self):
        self.MAX_THREADS = max(64, multiprocessing.cpu_count() * 4)
        self.MONITOR_POLL = 500
        self.MONITOR_TIME_UNIT = 'milli'
        self.ACTOR_MESSAGE_QUEUE_SIZE = 64
        self.ACTOR_MESSAGE_QUEUE_POLL = 500
        self.ACTOR_MESSAGE_QUEUE_OFFER = 5000
        self.ACTOR_MESSAGE_QUEUE_TIME_UNIT = 'milli'
        self.SHUTDOWN_WAIT = 10000
        self.SHUTDOWN_TIME_UNIT = 'milli'

    def set_max_threads(self, number):
        self.MAX_THREADS = number

    def set_monitor_poll(self, number):
        self.MONITOR_POLL = number

    def set_monitor_time_unit(self, unit):
        self.MONITOR_TIME_UNIT = unit

    def set_actor_message_queue_size(self, size):
        self.ACTOR_MESSAGE_QUEUE_SIZE = size

    def set_actor_message_queue_poll(self, number):
        self.ACTOR_MESSAGE_QUEUE_POLL = number

    def set_actor_message_queue_offer(self, number):
        self.ACTOR_MESSAGE_QUEUE_OFFER = number

    def set_actor_message_queue_time_unit(self, unit):
        self.ACTOR_MESSAGE_QUEUE_TIME_UNIT = unit

    def set_shutdown_wait(self, wait):
        self.SHUTDOWN_WAIT = wait

    def set_shutdown_time_unit(self, unit):
        self.SHUTDOWN_TIME_UNIT = unit
