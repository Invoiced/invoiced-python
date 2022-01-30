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


class TestContact(TestEndpoint, CreatableObject, RetrievableObject,
                  UpdatableObject, DeletableObject, ListAll,
                  unittest.TestCase):
    objectClass = invoiced.Contact
    endpoint = '/contacts'
