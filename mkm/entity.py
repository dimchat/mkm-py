#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
    MingKeMing Base
    ~~~~~~~~~~~~~~~

    Address, ID, Meta, Entity
"""

from mkm.address import Address


class ID(str):
    """
        ID for entity (Account/Group)
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        data format: "name@address[/terminal]"

        filed(s):
            name     - entity name, the seed of fingerprint to build address
            address  - a string to identify an entity
            terminal - entity login resource(device), OPTIONAL
    """

    name: str = ''
    address: Address = None
    terminal: str = ''

    def __new__(cls, string: str='',
                name: str='', address: Address=None, terminal: str=''):
        if string:
            # return ID object directory
            if isinstance(string, ID):
                return string
            # get fields from string
            pair = string.split('@', 1)
            name = pair[0]
            pair = pair[1].split('/', 1)
            address = Address(string=pair[0])
            if pair.__len__() > 1:
                terminal = pair[1]
            else:
                terminal = ''
        elif terminal:
            # concatenate address
            string = name + '@' + address + '/' + terminal
            address = Address(string=address)
        else:
            # concatenate address
            string = name + '@' + address
            address = Address(string=address)

        # new str
        self = super(ID, cls).__new__(cls, string)
        self.name = name
        self.address = address
        self.terminal = terminal
        return self

    def number(self) -> int:
        return self.address.number


class Entity:
    """
        Entity (Account / Group)
        ~~~~~~~~~~~~~~~~~~~~~~~~


    """

    ID: ID = None
    name: str = ''

    def __init__(self, entity_id):
        super(Entity, self).__init__()
        self.ID = entity_id
        self.name = ''

    def number(self) -> int:
        return self.ID.address.number
