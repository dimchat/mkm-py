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

    def cache_private_key(self, private_key: PrivateKey, identifier: ID):
        self.private_keys[identifier.address] = private_key

    def cache_meta(self, meta: Meta, identifier: ID):
        self.metas[identifier.address] = meta

    def cache_profile(self, profile: Profile, identifier: ID):
        self.profiles[identifier.address] = profile

    def cache_account(self, account: Account):
        if isinstance(account, User):
            self.cache_user(account)
            return
        if account.delegate is None:
            account.delegate = self
        self.accounts[account.identifier.address] = account

    def cache_user(self, user: User):
        if user.delegate is None:
            user.delegate = self
        self.users[user.identifier.address] = user

    def account(self, identifier: ID) -> Account:
        account = self.accounts.get(identifier.address)
        if account is None:
            account = self.users.get(identifier.address)
        # TODO: if account not found, create one?
        return account

    def user(self, identifier: ID) -> User:
        user = self.users.get(identifier.address)
        # TODO: if user not found, create one?
        return user

    #
    # Delegates
    #

    def private_key_for_signature(self, identifier: ID) -> PrivateKey:
        key = self.private_keys.get(identifier.address)
        return key

    def private_keys_for_decryption(self, identifier: ID) -> list:
        key = self.private_keys.get(identifier.address)
        return [key]

    def contacts(self, identifier: ID) -> list:
        # TODO: get contacts with user ID
        pass

    def meta(self, identifier: ID) -> Meta:
        return self.metas.get(identifier.address)

    def profile(self, identifier: ID) -> Profile:
        return self.profiles.get(identifier.address)


facebook = Facebook()

facebook.cache_private_key(private_key=moki_sk, identifier=moki_id)
facebook.cache_private_key(private_key=hulk_sk, identifier=hulk_id)

facebook.cache_meta(meta=moki_meta, identifier=moki_id)
facebook.cache_meta(meta=hulk_meta, identifier=hulk_id)

facebook.cache_profile(profile=moki_profile, identifier=moki_id)
facebook.cache_profile(profile=hulk_profile, identifier=hulk_id)

facebook.cache_user(User(moki_id))
facebook.cache_user(User(hulk_id))
