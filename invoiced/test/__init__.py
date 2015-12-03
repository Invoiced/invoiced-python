import os
import unittest


def all():
    path = os.path.dirname(os.path.realpath(__file__))
    print(path)
    return unittest.defaultTestLoader.discover(path)


def objects():
    path = os.path.dirname(os.path.realpath(__file__))
    return unittest.defaultTestLoader.discover(
        os.path.join(path, "objects"))
