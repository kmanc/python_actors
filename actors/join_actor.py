from actor import Actor, DoneMessage


class JoinActor(Actor):

    def __init__(self, key_list):
        super().__init__()
        self.key_list = key_list
        self.num_done = 0
        self.results = []

    def on_receive(self, message):
        if type(message) == DoneMessage:
            self.num_done += 1
            if self.num_done >= len(self.key_list):
                self.is_complete = True
        else:
            self.results.append(message)

    def on_complete(self):
        print(self.results)
