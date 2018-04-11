from actor import Actor, DoneMessage


class SplitterActor(Actor):

    def __init__(self, key_list):
        super().__init__()
        self.key_list = key_list
        self.loop = True

    def on_receive(self, message_list):
        while self.loop:
            for key in self.key_list:
                try:
                    instance = self.do_lookup(key)
                    instance.post(message_list.pop(0))
                except IndexError:
                    for needs_shutdown in self.key_list:
                        shut_me_down = self.do_lookup(needs_shutdown)
                        shut_me_down.post(DoneMessage())
                    self.is_complete = True
                    self.loop = False
