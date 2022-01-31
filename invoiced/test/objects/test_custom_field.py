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


class TestCustomField(TestEndpoint, CreatableObject, RetrievableObject,
                      UpdatableObject, DeletableObject, ListAll,
                      unittest.TestCase):
    objectClass = invoiced.CustomField
    endpoint = '/custom_fields'
