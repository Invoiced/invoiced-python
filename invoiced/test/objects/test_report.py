import unittest
import invoiced
from invoiced.test.objects.operations import (
    TestEndpoint,
    CreatableObject,
    RetrievableObject
)


class TestReport(TestEndpoint, CreatableObject, RetrievableObject,
                 unittest.TestCase):
    objectClass = invoiced.Report
    endpoint = '/reports'
