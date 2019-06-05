# -*- coding: utf-8 -*-

from mkm import *

from .immortals import *


class Facebook(IUserDataSource):

    def __init__(self):
        super().__init__()
        self.private_keys = {}
        self.metas = {}
        self.profiles = {}
        self.accounts = {}
        self.users = {}

    def add_private_key(self, private_key: PrivateKey, identifier: ID):
        self.private_keys[identifier.address] = private_key

    def add_meta(self, meta: Meta, identifier: ID):
        self.metas[identifier.address] = meta

    def add_profile(self, profile: Profile, identfier: ID):
        self.profiles[identfier.address] = profile

    def add_account(self, account: Account):
        if isinstance(account, User):
            self.add_user(account)
            return
        if account.delegate is None:
            account.delegate = self
        self.accounts[account.identifier.address] = account

    def account(self, identifier: ID) -> Account:
        account = self.accounts.get(identifier.address)
        if account is None:
            account = self.users.get(identifier.address)
        # TODO: if account not found, create one?
        return account

    def add_user(self, user: User):
        if user.delegate is None:
            user.delegate = self
        self.users[user.identifier.address] = user

    def user(self, identifier: ID) -> User:
        user = self.users.get(identifier.address)
        # TODO: if user not found, create one?
        return user

    #
    # Delegates
    #

    def user_private_key_for_signature(self, identifier: ID) -> PrivateKey:
        key = self.private_keys.get(identifier.address)
        return key

    def user_private_keys_for_decryption(self, identifier: ID) -> list:
        key = self.private_keys.get(identifier.address)
        return [key]

    def user_contacts(self, identifier: ID) -> list:
        # TODO: get contacts with user ID
        pass

    def entity_meta(self, identifier: ID) -> Meta:
        return self.metas.get(identifier.address)

    def entity_profile(self, identifier: ID) -> Profile:
        return self.profiles.get(identifier.address)


facebook = Facebook()

facebook.add_private_key(private_key=moki_sk, identifier=moki_id)
facebook.add_private_key(private_key=hulk_sk, identifier=hulk_id)

facebook.add_meta(meta=moki_meta, identifier=moki_id)
facebook.add_meta(meta=hulk_meta, identifier=hulk_id)

profile = Profile(identifier=moki_id)
profile.name = moki_name
profile.sign(private_key=moki_sk)
facebook.add_profile(profile=profile, identfier=moki_id)
profile = Profile(identifier=hulk_id)
profile.name = hulk_name
profile.sign(private_key=hulk_sk)
facebook.add_profile(profile=profile, identfier=hulk_id)

facebook.add_user(User(moki_id))
facebook.add_user(User(hulk_id))
