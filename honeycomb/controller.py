"""honeycomb.controller package"""

from __future__ import absolute_import, print_function, unicode_literals

import pygame
from pygame.locals import QUIT
from pygame.locals import KEYDOWN, KEYUP, K_ESCAPE
from pygame.locals import MOUSEBUTTONDOWN, MOUSEBUTTONUP

from .event import (
    TICK,
    QUIT as EV_QUIT,
    Event,
    EventListener,
    )

__metaclass__ = type
__all__ = [
    'Clock',
    'GameController',
    ]


class GameController(EventListener):
    KEYDOWN = {
        K_ESCAPE: 'quit',
        }
    KEYUP = {}
    MOUSEBUTTONDOWN = {}
    MOUSEBUTTONUP = {}

    def __init__(self, dispatcher):
        super(GameController, self).__init__()
        self.dispatcher = dispatcher
        self.dispatcher.register(self)

    def on_tick(self, event):
        for event in pygame.event.get():
            handler = None
            if event.type == QUIT:
                handler = 'quit'
            elif event.type == KEYDOWN:
                handler = self.KEYDOWN.get(event.key, None)
            elif event.type == KEYUP:
                handler = self.KEYUP.get(event.key, None)
            elif event.type == MOUSEBUTTONDOWN:
                handler = self.MOUSEBUTTONDOWN.get(event.button, None)
            elif event.type == MOUSEBUTTONUP:
                handler = self.MOUSEBUTTONUP.get(event.button, None)

            if handler:
                event = getattr(self, handler)(event)
                self.dispatcher.dispatch(event)

    def quit(self, event):
        return Event(EV_QUIT)


class Clock(EventListener):
    def __init__(self, dispatcher):
        super(Clock, self).__init__()
        self.dispatcher = dispatcher
        self.dispatcher.register(self)
        self.running = True

    def tick(self):
        while self.running:
            self.dispatcher.dispatch(Event(TICK))

    def on_quit(self, event):
        self.running = False
