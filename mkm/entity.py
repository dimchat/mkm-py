#! /usr/bin/env python
# -*- coding: utf-8 -*-

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
                name: str='', address: Address=None, terminal: str=None):
        """

        :param string:   ID string with format 'name@address/terminal'
        :param name:     A string for ID.name
        :param address:  An Address object for ID.address
        :param terminal: A string for login point
        :return:         ID object
        """
        if string:
            # return ID object directory
            if isinstance(string, ID):
                return string
            # get fields from string
            pair = string.split('@', 1)
            if len(pair) == 2:
                name = pair[0]
                pair = pair[1].split('/', 1)
                address = Address(pair[0])
                if len(pair) == 2:
                    terminal = pair[1]
                else:
                    terminal = None
            else:
                raise ValueError('Invalid ID string')
        elif name and address:
            # concatenate ID string
            address = Address(address)
            if terminal:
                string = name + '@' + address + '/' + terminal
            else:
                string = name + '@' + address
        else:
            raise AssertionError('Parameters error')
        # verify ID.address, which number must not be ZERO
        if address.number:
            # new str
            self = super(ID, cls).__new__(cls, string)
            self.name = name
            self.address = address
            self.terminal = terminal
            return self
        else:
            raise ValueError('Invalid ID (address) string')

    def number(self) -> int:
        return self.address.number


class Entity:
    """
        Entity (Account/Group)
        ~~~~~~~~~~~~~~~~~~~~~~

        Entity with ID and name
    """

    identity: ID = None
    name: str = ''

    def __init__(self, identity: ID):
        super(Entity, self).__init__()
        self.identity = identity
        self.name = identity.name

    def __str__(self):
        clazz = self.__class__.__name__
        identity = self.identity
        network = identity.address.network
        number = identity.address.number
        name = self.name
        return '<%s: %s(%d|%d) "%s">' % (clazz, identity, network, number, name)

    def number(self) -> int:
        return self.identity.address.number
