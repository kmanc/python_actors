from micro_kernel import MicroKernel
from actor import Actor
import time


class A(Actor):
    def on_receive(self, message):
        print(message)
        b = self.do_lookup("B")
        b.post("A is asking B to print this message")
        b.post("A also asks B to print this message")
        self.is_complete = True

    def get_name(self):
        return "A"


class B(Actor):
    def on_receive(self, message):
        time.sleep(3)
        print(message)

    def get_name(self):
        return "B"


kernel = MicroKernel()

a = A()
b = B()

kernel.submit(a)
kernel.submit(b)
a.post("I am asking A to print this message")

kernel.start()




