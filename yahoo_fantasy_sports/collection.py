from __future__ import absolute_import

from abc import ABCMeta
from six import add_metaclass


@add_metaclass(ABCMeta)
class Collection(object):
    """
    Base class for creating collections such as ``Games``, ``Leagues``, etc...
    """
