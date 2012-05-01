"""honeycomb.model package"""

from __future__ import absolute_import, print_function, unicode_literals

from .event import EventListener

__metaclass__ = type
__all__ = [
    'GameModel',
    ]


class GameModel(EventListener):
    def __init__(self, dispatcher):
        super(GameModel, self).__init__()
        self.dispatcher = dispatcher
        self.dispatcher.register(self)
