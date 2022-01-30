import unittest
import invoiced
from invoiced.test.objects.operations import (
    TestEndpoint,
    CreatableObject,
    RetrievableObject,
    DeletableObject
)


class TestFile(TestEndpoint, CreatableObject, RetrievableObject,
               DeletableObject, unittest.TestCase):
    objectClass = invoiced.File
    endpoint = '/files'
