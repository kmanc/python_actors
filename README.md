# Python Actors README

This library was made so you that you can use Python actors to achieve concurrency in your Python code.

If you are unfamiliar with the actor model, here is a quick rundown
* An actor is something capable of accepting a message, and performing work
* An actor can be a parent or a child to another actor
* Actors accept messages that are posted to them
* What an actor does with a message depends on the type of actor

## Generic Actor

A generic actor accepts messages, and can perform work on them. What work is performed
is dependent on the developer. Each actor has an `on_receive` method that must be defined
when the actor is defined. An actor's `on_receive` should be treated like any other function
in Python. An actor will continue to process messages until it is told it is complete, or until
it is shut down.

## Countdown Actor

A countdown actor is a special actor that is given a pre-determined number of messages to process
before completing when it is defined. Once it has processed that number of messages, it will shut down.
* NOTE: countdown actors do work in a `do_work` method; the `on_receive` is used by the countdown actor
class to accomplish its decrementing job characteristic.

## Split Actor

A split actor is a special actor that accepts an iterable message (list, dictionary, string, generator, etc)
and delegates individual messages to a list of child actors (which must be provided when the actor is defined).
Delegation is performed round-robin, and the split actor will take care of cleaning up the children actors
when it is complete.

## Batch Split Actor

A batch split actor is similar to a split actor, but will send lists of messages to child actors. This
allows for batching of a particular job. Batch split actors still accept an iterable message and are defined
with a list of children, and optionally a batch size (default is 256).

## Join actor

A join actor accepts messages from multiple parent actors and adds them to a list. When a join actor is defined, a
list of parent actors must be provided. When all parent actors have indicated that they are done sending messages,
the join actor complete.

## Getting data out of actors

You've defined your actor just the way you like it, but you want it to be able to return its results to your inline
code...how do you proceed? Well you'll have to go back to your actor definition, because this is a special use case,
but don't fret, it's not too bad. First, in your actor definition, redefine `__init__` for your actor such that it
accepts a new argument, cb. Then tell it to run its parent init (using `super().__init__([args])`), followed by setting
up its `self.cb = cb`. Basically what you're doing here is giving your actor a callback, which you can later use to "get
your results out". Now in your actors `on_complete` method, make the last line of code to execute `self.cb.callback(self.results)`.
When you instantiate your class, make sure you give it a CallbackFuture object (the CallbackFuture class can be imported from
actors.py), and after you have sent all of your work to the actor (and given it the signal that it is done), tell your code
to wait for the actor's results with `results = <callback_object_name>.done()`