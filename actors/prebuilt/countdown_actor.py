from actors.actor import Actor


class CountdownActor(Actor):

    def __init__(self, count):
        super().__init__()
        self.count = count

    def on_receive(self, message):
        self.do_work(message)
        self.count -= 1
        if self.count <= 0:
            self.is_complete = True

    @classmethod
    def do_work(cls, message):
        pass
