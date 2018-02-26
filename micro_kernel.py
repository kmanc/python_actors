import actor
import concurrent.futures
import micro_kernel_config


class MicroKernel(object):

    def __init__(self):
        self.is_running = True
        self.can_submit = True
        self.actor_lookup = dict()
        self.actor_future = dict()
        self.timer = 'timer'

        self.micro_kernel_config = micro_kernel_config.MicroKernelConfig()
        self.pool = concurrent.futures.Executor()
        self.monitor_future = 'something else'

    def submit(self, actor_instance):
        if self.can_submit:
            name = actor_instance.get_name()
            self.actor_lookup[name] = actor_instance
            actor_instance.__init__(self.actor_lookup, self.micro_kernel_config, self.timer)
            actor_instance.on_init()
            future = self.pool.submit(actor_instance)
            self.actor_future[name] = future
            return True
        else:
            return False

    def start(self):
        self.pool = concurrent.futures.ThreadPoolExecutor(self.micro_kernel_config.MAX_THREADS)

    def shutdown(self):
        print('microkernel shut down')
