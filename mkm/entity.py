# -*- coding: utf-8 -*-
#
#   Ming-Ke-Ming : Decentralized User Identity Authentication
#
#                                Written in 2019 by Moky <albert.moky@gmail.com>
#
# ==============================================================================
# MIT License
#
# Copyright (c) 2019 Albert Moky
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ==============================================================================

from abc import abstractmethod, ABCMeta

from .address import NetworkID
from .identifier import ID
from .meta import Meta
from .profile import Profile


class IEntityDataSource(metaclass=ABCMeta):
    """
        Entity Data Source
        ~~~~~~~~~~~~~~~~~~
    """

    @abstractmethod
    def meta(self, identifier: ID) -> Meta:
        """
        Get meta for entity ID

        :param identifier: entity ID
        :return:           meta info
        """
        pass

    @abstractmethod
    def profile(self, identifier: ID) -> Profile:
        """
        Get profile for entity ID

        :param identifier: entity ID
        :return:           profile info
        """
        pass


class Entity:
    """Base class of User and Group, ...

        Entity (User/Group)
        ~~~~~~~~~~~~~~~~~~~

            properties:
                identifier - entity ID
                type       - entity type
                number     - search number
                meta       - meta for entity ID
                profile    - entity profile
                name       - nickname
    """

    def __init__(self, identifier: ID):
        """
        Create Entity with ID

        :param identifier: User/Group ID
        """
        super().__init__()
        self.__identifier: ID = identifier
        self.__delegate: IEntityDataSource = None

    def __str__(self):
        clazz = self.__class__.__name__
        identifier = self.__identifier
        network = identifier.address.network
        number = identifier.address.number
        name = self.name
        return '<%s: %s(%d|%d) "%s" />' % (clazz, identifier, network, number, name)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Entity):
            return False
        return self.__identifier == other.identifier

    @property
    def identifier(self) -> ID:
        return self.__identifier

    @property
    def type(self) -> NetworkID:
        """ Entity type """
        return self.__identifier.address.network

    @property
    def number(self) -> int:
        """ Search number of this entity """
        return self.__identifier.address.number

    @property
    def name(self) -> str:
        # get from profile
        profile = self.profile
        if profile is not None:
            name = profile.name
            if name is not None:
                return name
        # get from identifier
        return self.__identifier.name

    @property
    def meta(self) -> Meta:
        return self.delegate.meta(identifier=self.__identifier)

    @property
    def profile(self) -> Profile:
        return self.delegate.profile(identifier=self.__identifier)

    @property
    def delegate(self) -> IEntityDataSource:
        return self.__delegate

    @delegate.setter
    def delegate(self, value):
        self.__delegate = value
