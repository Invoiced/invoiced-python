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


class TestTheme(TestEndpoint, CreatableObject, RetrievableObject,
                UpdatableObject, DeletableObject, ListAll,
                unittest.TestCase):
    objectClass = invoiced.Theme
    endpoint = '/themes'
