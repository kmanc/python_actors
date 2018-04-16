from actors.actor import Actor, DoneMessage, FlushMessage
from log_config import actor_logger


class BatchSplitActor(Actor):

    def __init__(self, key_list, batch_size=256):
        super().__init__()
        self.key_list = key_list
        self.loop = True
        self.batch_size = batch_size
        self.batch_dict = dict(zip(key_list, [[] for i in range(len(key_list))]))

    def on_receive(self, message):
        if type(message) == DoneMessage:
            for key in self.key_list:
                instance = self.do_lookup(key)
                instance.post(self.batch_dict[key])
                instance.post(DoneMessage())
            self.is_complete = True
        elif type(message) == FlushMessage:
            for key in self.key_list:
                instance = self.do_lookup(key)
                instance.post(self.batch_dict[key])
                self.batch_dict[key] = []
        else:
            try:
                message_iterable = iter(message)
                while self.loop:
                    for key in self.key_list:
                        self.batch_dict[key].append(next(message_iterable))
                        if len(self.batch_dict[key]) >= self.batch_size:
                            instance = self.do_lookup(key)
                            instance.post(self.batch_dict[key])
                            self.batch_dict[key] = []
            except IndexError:
                self.loop = False
            except TypeError:
                actor_logger.error(f'{self.name} was given a non-iterable message')
                self.shutdown()
