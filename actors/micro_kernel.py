import concurrent.futures
from actors.actor import Actor


class MicroKernel(object):

    def __init__(self):
        self.is_running = True
        self.can_submit = True
        self.actor_lookup = dict()
        self.actor_future = dict()
        self.pool = concurrent.futures.ThreadPoolExecutor()
        self.monitor_future = concurrent.futures.Future()

    def submit(self, name, actor_instance):
        if self.can_submit:
            actor_instance.name = name
            self.actor_lookup[name] = actor_instance
            actor_instance.on_init(self.actor_lookup)
            self.actor_future[name] = self.pool.submit(Actor.call, actor_instance)
            return True
        else:
            return False

    def post(self, name, message):
        actor = self.actor_lookup[name]
        actor.post(message)

    def start(self):
        self.monitor_future = self.pool.submit(self.monitor, self)

    @staticmethod
    def monitor(kernel):
        while kernel.is_running and bool(kernel.actor_future):
            for actor_name in list(kernel.actor_future):
                try:
                    is_complete = kernel.actor_future[actor_name].result(timeout=5)
                    actor = kernel.actor_lookup[actor_name]
                    del kernel.actor_future[actor_name]
                    del kernel.actor_lookup[actor_name]
                    if is_complete is True:
                        actor.on_complete()
                except concurrent.futures.TimeoutError:
                    print(f'Actor(s) {", ".join(list(kernel.actor_future))} has/have not completed yet')
        kernel.is_running = False
        return True

    def shutdown(self, wait=False):
        self.can_submit = False
        self.pool.shutdown(wait=wait)
        self.is_running = False
        for entry in self.actor_lookup.values():
            entry.shutdown()
        return
