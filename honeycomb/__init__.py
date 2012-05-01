"""honeycomb package"""

from __future__ import absolute_import, print_function, unicode_literals

from .controller import Clock
from .event import INIT
from .event import Event, EventDispatcher

__metaclass__ = type
__all__ = [
    'Game',
    ]


class Game(EventDispatcher):
    def __init__(self, name):
        super(Game, self).__init__()

        self.models = []
        self.views = []
        self.controllers = []

        self.clock = Clock(self)

    def add_controller(self, controller):
        self.controllers.append(controller(self))

    def add_view(self, view):
        self.views.append(view(self))

    def add_model(self, model):
        self.models.append(model(self))

    def run(self):
        self.dispatch(Event(INIT))
        self.clock.tick()
