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
the join actor will send the list back to ____ and complete.