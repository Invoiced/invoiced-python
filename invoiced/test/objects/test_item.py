import unittest
import invoiced
from invoiced.test.objects.operations import (
    TestEndpoint,
    CreatableObject,
    RetrievableObject,
    UpdatableObject,
    DeletableObject,
    ListAll
)


class TestItem(TestEndpoint, CreatableObject, RetrievableObject,
               UpdatableObject, DeletableObject, ListAll,
               unittest.TestCase):
    objectClass = invoiced.Item
    endpoint = '/items'
