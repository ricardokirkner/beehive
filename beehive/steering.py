"""beehive.steering package"""
from __future__ import absolute_import, print_function, unicode_literals

__metaclass__ = type
__all__ = [
    'Flee',
    'Seek',
    'Steering',
    ]

from .core import Behaviour
from .geometry import Vector3


class Steering(Behaviour):
    sensors = ['target']
    actuators = ['force']

    def __call__(self, dt):
        if self.agent.target is None:
            return ('force', Vector3())
        return self.steer(self.agent.target)


class Seek(Steering):
    sensors = Steering.sensors + ['position', 'velocity']

    def steer(self, target):
        desired_velocity = target - self.agent.position
        force = desired_velocity - self.agent.velocity
        return ('force', force)


class Flee(Steering):
    sensors = Steering.sensors + ['position', 'velocity']

    def steer(self, target):
        desired_velocity = self.agent.position - target
        force = desired_velocity - self.agent.velocity
        return ('force', force)
