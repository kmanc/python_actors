import micro_kernel_config
import queue


class Actor(object):

    def __init__(self):
        self.is_running = True
        self.is_complete = False
        self.message_queue = queue.Queue()
        self.actor_lookup = dict()
        self.timer = 'timer'

        self.config = micro_kernel_config.MicroKernelConfig()

    def on_receive(self, message):
        print('on receive')

    def get_name(self):
        print('get name')

    def on_init(self):
        print('on init')

    def on_complete(self):
        print('on complete')

    def on_shutdown(self):
        print('on shutdown')

    def call(self):
        print('call')

    def post(self):
        print('on receive')

    def schedule(self):
        print('schedule')

    def do_lookup(self):
        print('lookup')

    def shutdown(self):
        print('shutdown')

    def set_complete(self):
        print('set complete')
