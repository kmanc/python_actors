import concurrent.futures
import micro_kernel_config
from actor import Actor


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
            actor_instance.on_init(self.actor_lookup, self.micro_kernel_config)
            self.actor_future[name] = self.pool.submit(Actor.call, actor_instance)
            return True
        else:
            return False

    def post(self, name, message):
        actor = self.actor_lookup(name)
        actor.post(message)

    def start(self):
        self.monitor_future = self.pool.submit(self.monitor, self)

    @staticmethod
    def monitor(kernel):
        while kernel.is_running or bool(kernel.actor_future):
            for key, value in kernel.actor_future.items():
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

    def shutdown(self):
        self.can_submit = False
        self.is_running = False
        for entry in self.actor_lookup.values():
            entry.shutdown()
        self.pool.shutdown()

