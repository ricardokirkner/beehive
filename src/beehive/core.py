"""beehive.core package"""
from __future__ import absolute_import, print_function, unicode_literals

__metaclass__ = type
__all__ = [
    'Agent',
    'Behaviour',
    'Body',
    'Shape',
    'World',
    ]

import heapq
import time

from .geometry import Vector2


class Behaviour:
    def __init__(self, agent):
        self.agent = agent

    def update(self, dt):
        if self.agent.target is None:
            return Vector2()

        target = self.agent.target
        return self.steer(target)


class Body:
    def __init__(self):
        self.mass = 1.0
        self.position = Vector2()
        self.velocity = Vector2()
        self.max_speed = 1.0
        self.max_force = 0.1
        self.acceleration = Vector2()

    def update(self, force):
        self.acceleration = force / self.mass
        # clip acceleration
        if self.acceleration.magnitude_squared() > self.max_force ** 2:
            self.acceleration *= (self.max_force / abs(self.acceleration))

        self.velocity += self.acceleration
        # clip velocity
        if self.velocity.magnitude_squared() > self.max_speed ** 2:
            self.velocity *= (self.max_speed / abs(self.velocity))

        self.position += self.velocity

    @property
    def forward(self):
        return self.orientation

    @property
    def speed(self):
        return abs(self.velocity)


class Agent:
    def __init__(self, body=None):
        self.behaviours = []
        if body is None:
            body = Body()
        self.body = body
        self._last_t = time.time()
        self.target = None

    def learn(self, weight, behaviour):
        heapq.heappush(self.behaviours, (weight, behaviour(self)))

    @apply
    def position():
        def fget(self):
            return self.body.position
        def fset(self, value):
            self.body.position = value
        return property(**locals())

    @apply
    def velocity():
        def fget(self):
            return self.body.velocity
        def fset(self, value):
            self.body.velocity = value
        return property(**locals())

    def update(self):
        now = time.time()
        dt = now - self._last_t
        self._last_t = now

        # get behaviour to run
        behaviour = heapq.nlargest(1, self.behaviours)[0][1]

        # apply behaviour
        force = behaviour.update(dt)
        self.body.update(force)


class World:
    def update(self):
        """Update all agents in the world."""

    @property
    def size(self):
        """Return a 3-dimensional vector indicating the size of the world."""


class Shape:
    def draw(self, screen, position):
        """Draw the shape onto the screen at the given position."""
