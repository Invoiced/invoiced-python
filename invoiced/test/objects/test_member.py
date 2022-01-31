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


class TestMember(TestEndpoint, CreatableObject, RetrievableObject,
                 UpdatableObject, DeletableObject, ListAll,
                 unittest.TestCase):
    objectClass = invoiced.Member
    endpoint = '/members'
