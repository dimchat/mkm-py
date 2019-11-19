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

"""
    Group for assembly
    ~~~~~~~~~~~~~~~~~~

    Group with members
"""

from typing import Optional

from .identifier import ID
from .entity import Entity
from .delegate import GroupDataSource


class Group(Entity):
    """This class is for creating group

        Group for organizing users
        ~~~~~~~~~~~~~~~~~~~~~~~~~~

            roles:
                founder
                owner
                members
                administrators - Optional
                assistants     - Optional
    """

    def __init__(self, identifier: ID):
        super().__init__(identifier=identifier)
        # once the group founder is set, it will never change
        self.__founder: ID = None

    @Entity.delegate.getter
    def delegate(self) -> Optional[GroupDataSource]:
        facebook = super().delegate
        assert facebook is None or isinstance(facebook, GroupDataSource), 'error: %s' % facebook
        return facebook

    # @delegate.setter
    # def delegate(self, value: GroupDataSource):
    #     super(Group, Group).delegate.__set__(self, value)

    @property
    def founder(self) -> Optional[ID]:
        if self.__founder is None:
            self.__founder = self.delegate.founder(identifier=self.identifier)
        return self.__founder

    @property
    def owner(self) -> Optional[ID]:
        return self.delegate.owner(identifier=self.identifier)

    @property
    def members(self) -> Optional[list]:
        return self.delegate.members(identifier=self.identifier)
