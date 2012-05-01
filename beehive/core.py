"""beehive.core package"""
from __future__ import absolute_import, print_function, unicode_literals

__metaclass__ = type
__all__ = [
    'Agent',
    'Behaviour',
    'Body',
    'POM',
    'SimpleVehicle',
    ]

import heapq
import time

from .geometry import Vector3


class Behaviour:
    sensors = []
    actuators = []

    def __init__(self, agent):
        missing_sensors = set(self.sensors) - set(agent.body.sensors)
        missing_actuators = set(self.actuators) - set(agent.body.actuators)
        if missing_sensors or missing_actuators:
            missing = ''
            if missing_sensors:
                missing += "sensors=%r, " % missing_sensors
            if missing_actuators:
                missing += "actuators=%r" % missing_actuators
            msg = ("Agent does not conform to required API. "
                "Missing: %s" % missing)
            raise Exception(msg)
        self.agent = agent

    def __call__(self, dt):
        raise NotImplementedError()


class Body:
    @property
    def sensors(self):
        """Return list of available sensors."""

    @property
    def actuators(self):
        """Return list of available actuators."""


class POM(Body):
    """Body representing a Point-Of-Mass model."""

    @property
    def sensors(self):
        return [
            'acceleration',
            'mass',
            'position',
            'velocity',
            ]

    @property
    def actuators(self):
        return [
            'force',
            ]


class SimpleVehicle(POM):
    """A simple vehicle, based on the Point-Of-Mass model."""

    def __init__(self):
        super(SimpleVehicle, self).__init__()
        # POM API
        self._acceleration = Vector3()
        self._mass = 1.0
        self._velocity = Vector3()
        self.position = Vector3()
        self.target = Vector3()

        # physical limitations of body
        self.max_force = 0.1
        self.max_speed = 1.0

    # Body API
    @property
    def sensors(self):
        return super(SimpleVehicle, self).sensors + ['target']
    # Body API

    # POM API
    @property
    def acceleration(self):
        return self._acceleration

    @property
    def mass(self):
        return self._mass

    @property
    def velocity(self):
        return self._velocity

    @apply
    def force():
        def fset(self, value):
            self._acceleration = value / self.mass
            # clip acceleration
            if self._acceleration.magnitude_squared() > self.max_force ** 2:
                self._acceleration *= (self.max_force / abs(self._acceleration))

            self._velocity += self._acceleration
            # clip velocity
            if self._velocity.magnitude_squared() > self.max_speed ** 2:
                self._velocity *= (self.max_speed / abs(self._velocity))

            self.position += self._velocity
        return property(None, fset)
    # POM API


class Agent:
    __attributes = [
        '_last_t',
        'behaviours',
        'body',
        ]

    def __init__(self, body=None):
        self._last_t = time.time()
        self.behaviours = []
        if body is None:
            body = Body()
        self.body = body

    def __getattr__(self, name):
        if name in self.__attributes:
            return super(Agent, self).__getattr__(name)
        # proxy attribute lookup to the body
        return getattr(self.body, name)

    def __setattr__(self, name, value):
        if name in self.__attributes:
            super(Agent, self).__setattr__(name, value)
        else:
            # proxy attribute setting to the body
            setattr(self.body, name, value)

    def learn(self, weight, behaviour):
        try:
            heapq.heappush(self.behaviours, (weight, behaviour(self)))
        except:
            # ignore behaviour as the agent doesn't conform to the required API
            pass

    def update(self):
        now = time.time()
        dt = now - self._last_t
        self._last_t = now

        # get behaviour to run
        ## get maximum weight behaviour
        weight = self.behaviours[-1][0]
        ## get all behaviours with same weight
        selected = [b for (w, b) in self.behaviours if w == weight]
        # apply behaviours
        results = [behaviour(dt) for behaviour in selected]
        for (actuator, value) in results:
            setattr(self.body, actuator, value)
