import actor
import concurrent.futures
import micro_kernel_config


class MicroKernel(object):

    def __init__(self):
        self.micro_kernel_config = micro_kernel_config.MicroKernelConfig()

        self.is_running = True
        self.can_submit = True
        self.actor_lookup = dict()
        self.actor_future = dict()
        self.pool = concurrent.futures.ThreadPoolExecutor(self.micro_kernel_config.MAX_THREADS)
        self.monitor_future = concurrent.futures.Future()

    def submit(self, actor_instance):
        if self.can_submit:
            name = actor_instance.get_name()
            self.actor_lookup[name] = actor_instance
            actor_instance.__init__(self.actor_lookup, self.micro_kernel_config)
            actor_instance.on_init()
            self.actor_future[name] = self.pool.submit(actor_instance)
            return True
        else:
            return False

    def start(self):
        monitor = callable()

        #@Override
        def call():

            while self.is_running or bool(self.actor_future):
                for key, value in self.actor_future.items():
                    future = value
                    is_remove = False
                    try:
                        obj = future.result()
                        is_remove = True
                    except TimeoutError:
                        pass
                    if is_remove:
                        value.on_complete()

            return None

        self.monitor_future = self.pool.submit(monitor)

    def shutdown(self):
        self.can_submit = False
        self.is_running = False
        for entry in self.actor_lookup.values():
            entry.shutdown()
        self.pool.shutdown()
