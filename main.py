from actor import Actor
from actors.countdown_actor import CountdownActor
from micro_kernel import MicroKernel
import time


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


class C(CountdownActor):
    def do_work(self, message):
        time.sleep(2)
        print(message)


kernel = MicroKernel()

a = A()
b = B(count=6)
c = C(count=6)

kernel.submit("A", a)
kernel.submit("B", b)
kernel.submit("C", c)
a.post("I am asking A to print this message")

kernel.start()
print('Calling shutdown')
kernel.shutdown(True)
print('Kernel has shut down')
