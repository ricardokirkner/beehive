"""honeycomb.view package"""

from __future__ import absolute_import, print_function, unicode_literals

import pygame

from .event import EventListener

__metaclass__ = type
__all__ = [
    'GameView',
    ]


class GameView(EventListener):
    def __init__(self, dispatcher, width, height):
        super(GameView, self).__init__()
        self.dispatcher = dispatcher
        self.dispatcher.register(self)

        self.width = width
        self.height = height

    def on_init(self, event):
        pygame.init()

        self.window = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.Surface(self.window.get_size())
        self.background.fill((0, 0, 0))

    def on_tick(self, event):
        pygame.display.flip()
        self.window.blit(self.background, (0, 0))
