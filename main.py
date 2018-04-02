from micro_kernel import MicroKernel
from actor import Actor
import time


class A(Actor):
    def on_receive(self, message):
        print(message)
        b = self.do_lookup("B")
        c = self.do_lookup("C")
        b.post("A is asking B to print this message")
        b.post("A also asks B to print this message")
        b.post("and another")
        b.post("and another another")
        b.post("and another another another")
        b.post("and another another another another")
        c.post("A is asking C to print this message")
        c.post("A also asks C to print this message")
        c.post("and C")
        c.post("and C C")
        c.post("and C C C")
        c.post("and C C C C")
        if self.message_queue.empty():
            self.is_complete = True

    def get_name(self):
        return "A"


class B(Actor):
    def on_receive(self, message):
        time.sleep(2)
        print(message)
        if self.message_queue.empty():
            self.is_complete = True

    def get_name(self):
        return "B"


class C(Actor):
    def on_receive(self, message):
        time.sleep(2)
        print(message)
        if self.message_queue.empty():
            self.is_complete = True

    def get_name(self):
        return "C"


kernel = MicroKernel()

a = A()
b = B()
c = C()

kernel.submit(a)
kernel.submit(b)
kernel.submit(c)
a.post("I am asking A to print this message")

kernel.start()
