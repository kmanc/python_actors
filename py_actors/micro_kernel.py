import concurrent.futures
from py_actors.actors import Actor
from py_actors.log_config import actor_logger


class MicroKernel(object):
    """A basic kernel to run actors in"""

    def __init__(self):
        self.monitor_future = None
        self.is_running = True
        self.can_submit = True
        self.actor_lookup = dict()
        self.actor_future = dict()
        self.pool = concurrent.futures.ThreadPoolExecutor()

    def submit(self, name, actor_instance):
        """Put an actor instance into the kernel"""
        if self.can_submit:
            actor_instance.name = name
            self.actor_lookup[name] = actor_instance
            actor_instance.on_init(self.actor_lookup)
            self.actor_future[name] = self.pool.submit(Actor.call, actor_instance)
            return True
        else:
            return False

    def post(self, name, message):
        """Send a message to an actor"""
        actor = self.actor_lookup[name]
        actor.post(message)

    def start(self):
        """Start the kernel"""
        self.monitor_future = self.pool.submit(self.monitor, self)

    @staticmethod
    def monitor(kernel):
        """Process message queues for actors in the kernel"""
        while kernel.is_running or bool(kernel.actor_future):
            for actor_name in list(kernel.actor_future):
                try:
                    is_complete = kernel.actor_future[actor_name].result(timeout=5)
                    actor = kernel.actor_lookup[actor_name]
                    del kernel.actor_future[actor_name]
                    del kernel.actor_lookup[actor_name]
                    if is_complete is True:
                        actor.on_complete()
                except concurrent.futures.TimeoutError:
                    actor_logger.debug(f'Actor(s) {", ".join(list(kernel.actor_future))} has/have not completed yet')
        return True

    def shutdown(self, immediate=True):
        """Shut the kernel down. When immediate is set to True, all active actors will be terminated, and unprocessed
        messages will be dropped. If immediate is set to False, actors will finish processing all messages in their
        queue at the time shutdown was called
        """
        self.can_submit = False
        self.is_running = False
        if immediate:
            actor_logger.debug(f'Shutting down {list(self.actor_lookup)} preemptively')
            for entry in self.actor_lookup.values():
                entry.shutdown()
        self.pool.shutdown()
        return
