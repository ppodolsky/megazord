"""
Interstate stores caching data in .megazord subfolder
"""

import os
import pickle
import megazord


def clear():
    destroy()
    init()


def destroy():
    megazord.system.rm('.megazord')


def init():
    if is_init():
        raise FileExistsError('Megazord already initialized')
    else:
        megazord.system.mkdir_p('.megazord')
        megazord.system.mkdir_p('.megazord/targets')


def is_init():
    return megazord.system.exists('.megazord')


def mzdir(path):
    return ".megazord/{}".format(path)


def load_object(path):
    if not megazord.system.exists(mzdir(path)):
        return None
    else:
        f = open(mzdir(path), "rb")
        result = pickle.load(f)
    return result


def save_object(path, obj):
    with open(mzdir(path), "wb+") as f:
        result = pickle.dump(obj, f)
    return result


def load_target_info(name):
    return load_object("{}/{}".format('targets', name))


def save_target_info(name, obj):
    return save_object("{}/{}".format('targets', name), obj)


class TargetInfo:
    def __init__(self, name):
        self.name = name
        self.target_info = load_target_info(self.name)
        if self.target_info is None:
            save_target_info(self.name, {})
            self.target_info = {}

    def __getitem__(self, index):
        if index not in self.target_info:
            return None
        else:
            return self.target_info[index]

    def __setitem__(self, index, value):
        self.target_info[index] = value
        save_target_info(self.name, self.target_info)


class TargetStorage:
    def __getitem__(self, index):
        return TargetInfo(index)

if not is_init():
    init()
target_storage = TargetStorage()