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


class TestRole(TestEndpoint, CreatableObject, RetrievableObject,
               UpdatableObject, DeletableObject, ListAll,
               unittest.TestCase):
    objectClass = invoiced.Role
    endpoint = '/roles'
