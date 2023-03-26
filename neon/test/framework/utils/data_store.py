import os

import greenlet


class DictObject(dict):

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError("'{0}' object has no attribute '{1}'".format(self.__class__.__name__, name))

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        try:
            del self[name]
        except KeyError:
            raise AttributeError("'{0}' object has no attribute '{1}'".format(self.__class__.__name__, name))


class DataStoreContainer(object):

    user = {}

    def __init__(self):
        self.__scenario = DictObject()
        self.__spec = DictObject()
        self.__suite = DictObject()

    @property
    def scenario(self):
        return self.__scenario

    @property
    def spec(self):
        return self.__spec

    @property
    def suite(self):
        return self.__suite


def __get_user():
    try:
        return greenlet.getcurrent().minimal_ident + 1
    except Exception:
        return 0


def get_instance():
    user_id = __get_user()
    DataStoreContainer.user[user_id] = DataStoreContainer.user.get(user_id, DataStoreContainer())
    return DataStoreContainer.user[user_id]


if os.getenv('testType', 'functional') == 'functional':
    from getgauge.python import data_store
    data = data_store
else:
    data = DataStoreContainer()
