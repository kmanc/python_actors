import time
from actors.actor import Actor, DoneMessage
from actors.micro_kernel import MicroKernel
from actors.prebuilt.batch_split_actor import BatchSplitActor
from actors.prebuilt.countdown_actor import CountdownActor
from actors.prebuilt.join_actor import JoinActor
from actors.prebuilt.split_actor import SplitActor


class A(Actor):
    def on_receive(self, message):
        print(message)
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
        time.sleep(2)
        print(message)


class C(Actor):
    def on_receive(self, message):
        if type(message) == DoneMessage:
            g = self.do_lookup("G")
            g.post(DoneMessage())
            self.is_complete = True
        else:
            g = self.do_lookup("G")
            g.post(message)


kernel = MicroKernel()

a = A()
b = B(count=6)
c = B(count=6)
d = C()
e = C()
f = SplitActor(["D", "E"])
g = JoinActor(["D", "E"])

kernel.submit("A", a)
kernel.submit("B", b)
kernel.submit("C", c)
kernel.submit("D", d)
kernel.submit("E", e)
kernel.submit("F", f)
kernel.submit('G', g)

kernel.start()
a.post("I am asking A to print this message")
messages = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
f.post(messages)
f.post(DoneMessage())
kernel.shutdown(True)
