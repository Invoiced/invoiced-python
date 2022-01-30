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


class TestLineItem(TestEndpoint, CreatableObject, RetrievableObject,
                   UpdatableObject, DeletableObject, ListAll,
                   unittest.TestCase):
    objectClass = invoiced.LineItem
    endpoint = '/line_items'
