"""beehive.steering package"""
from __future__ import absolute_import, print_function, unicode_literals

__metaclass__ = type
__all__ = [
    'Seek',
    ]

from .core import Behaviour


class Seek(Behaviour):
    def steer(self, target):
        desired_velocity = target - self.agent.position
        return desired_velocity - self.agent.velocity
