import time
from actors.actor import Actor, CallbackFuture, DoneMessage, FlushMessage
from actors.micro_kernel import MicroKernel
from actors.prebuilt.batch_split_actor import BatchSplitActor
from actors.prebuilt.countdown_actor import CountdownActor
from actors.prebuilt.join_actor import JoinActor
from actors.prebuilt.split_actor import SplitActor
from actors.log_config import actor_logger


class A(Actor):
    def on_receive(self, message):
        actor_logger.debug(message)
        b = self.do_lookup("B")
        c = self.do_lookup("C")
        b.post("A is asking B to print this message")
        b.post("A also asks B to print this message")
        b.post("and B")
        b.post("and B B")
        b.post("and B B B")
        b.post("and B B B B")
        c.post("A is asking C to print this message")
        c.post("A also asks C to print this message")
        c.post("and C")
        c.post("and C C")
        c.post("and C C C")
        c.post("and C C C C")
        self.is_complete = True


class B(CountdownActor):
    def do_work(self, message):
        time.sleep(1)
        actor_logger.debug(message)


class C(Actor):
    def on_receive(self, message):
        if type(message) == DoneMessage:
            g = self.do_lookup("G")
            g.post(DoneMessage())
            self.is_complete = True
        else:
            g = self.do_lookup("G")
            g.post(message)


class D(Actor):
    def on_receive(self, message):
        if type(message) == DoneMessage:
            g = self.do_lookup("K")
            g.post(DoneMessage())
            self.is_complete = True
        else:
            g = self.do_lookup("K")
            g.post(message)


class E(JoinActor):
    def __init__(self, key_list, cb):
        super().__init__(key_list)
        self.cb = cb

    def on_complete(self):
        self.cb.callback(self.results)
        actor_logger.info(f'{self.name} has finished')


class TestActors:
    def test_system(self):
        # Kernel for running actors
        kernel = MicroKernel()
        kernel.start()

        # Things that will be used for control flow
        flush = FlushMessage()
        done = DoneMessage()

        # Callback object for "getting data out"
        call = CallbackFuture()

        # Test general use actors, and countdown actors by having a general use actor send messages to countdown actors
        # Also starts the kernel now that we have some messages to process
        a = A()
        b = B(count=6)
        c = B(count=6)

        kernel.submit("A", a)
        kernel.submit("B", b)
        kernel.submit("C", c)
        a.post("I am asking A to print this message")

        # Test splitting and joining actors by having a split actor send messages to generic actors, and a join actor
        # accept messages from those generic actors
        d = C()
        e = C()
        f = SplitActor(["D", "E"])
        g = JoinActor(["D", "E"])

        kernel.submit("D", d)
        kernel.submit("E", e)
        kernel.submit("F", f)
        kernel.submit('G', g)
        messages = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
        f.post(messages)
        f.post(done)

        # Test batch splitting actor and callbacks by having the batch splitter create batches for two generic actors,
        # which send their messages to a join actor. This join actor accepts a callback, and returns its results to the
        # inline code
        h = D()
        i = D()
        j = BatchSplitActor(["H", "I"], batch_size=4)
        k = E(["H", "I"], call)

        kernel.submit('H', h)
        kernel.submit('I', i)
        kernel.submit('J', j)
        kernel.submit('K', k)

        batch = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
        j.post(batch)
        j.post(flush)
        j.post([20])
        j.post(done)
        results = call.done()
        actor_logger.info(f'The joiner is done: {results}')

        # Shut down the kernel
        kernel.shutdown(immediate=False)

        # Make sure things ran correctly
        try:
            assert len(results) == 20
            assert a.is_complete is True
            assert b.is_complete is True
            assert c.is_complete is True
            assert d.is_complete is True
            assert e.is_complete is True
            assert f.is_complete is True
            assert g.is_complete is True
            assert h.is_complete is True
            assert i.is_complete is True
            assert j.is_complete is True
            assert k.is_complete is True
        except AssertionError:
            actor_logger.error(f'One of the test cases failed')
            exit(0)
