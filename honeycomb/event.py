"""honeycomb.event package"""

from __future__ import absolute_import, print_function, unicode_literals

from weakref import WeakKeyDictionary

__metaclass__ = type
__all__ = [
    'INIT',
    'TICK',
    'QUIT',
    'Event',
    'EventListener',
    'EventDispatcher',
    ]

# standard events
INIT = 'init'
QUIT = 'quit'
TICK = 'tick'

class Event:
    def __init__(self, name='event', **kwargs):
        self.name = name
        self.__dict__.update(**kwargs)


class EventListener:
    def on_event(self, event):
        handler = getattr(self, 'on_%s' % event.name, None)
        if handler:
            handler(event)


class EventDispatcher:
    def __init__(self):
        self.listeners = WeakKeyDictionary()

    def register(self, listener):
        self.listeners[listener] = 1

    def unregister(self, listener):
        if listener in self.listeners:
            del self.listeners[listener]

    def dispatch(self, event):
        for listener in self.listeners:
            listener.on_event(event)
