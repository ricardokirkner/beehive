"""beehive.geometry package"""
from __future__ import absolute_import, print_function, unicode_literals

__metaclass__ = type
__all__ = [
    'Vector2',
    'Vector3',
    ]

# import into local namespace
from . import euclid

Vector2 = euclid.Vector2
Vector3 = euclid.Vector3
