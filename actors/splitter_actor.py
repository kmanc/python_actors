from actor import Actor


class SplitterActor(Actor):

    def __init__(self):
        super().__init__()

    def on_receive(self, message):
        # DOESNT WORK YET
        print(message)

    @classmethod
    def do_work(cls, message):
        pass
