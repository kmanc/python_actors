from actors.actor import Actor, DoneMessage
from log_config import actor_logger


class SplitActor(Actor):

    def __init__(self, key_list):
        super().__init__()
        self.key_list = key_list
        self.loop = True

    def on_receive(self, message):
        if type(message) == DoneMessage:
            self.is_complete = True
        else:
            try:
                message_iterable = iter(message)
                while self.loop:
                    for key in self.key_list:
                        instance = self.do_lookup(key)
                        instance.post(next(message_iterable))
            except StopIteration:
                for needs_shutdown in self.key_list:
                    shut_me_down = self.do_lookup(needs_shutdown)
                    shut_me_down.post(DoneMessage())
                self.loop = False
            except TypeError:
                actor_logger.error(f'{self.name} was given a non-iterable message')
                exit(0)
