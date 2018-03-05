from micro_kernel import MicroKernel
from actor import Actor


class A(Actor):
    def on_receive(self, message):
        print(message)
        b = self.do_lookup("B")
        b.post( "you smell" )

    def get_name(self):
        return "A"

class B(Actor):
    def on_receive(self, message):
        print(message)

    def get_name(self):
        return "B"

kernel = MicroKernel()

a = A()
b = B()

kernel.submit(a)
kernel.submit(b)
a.post("doesn't matter cos a prints ping")

kernel.start()




