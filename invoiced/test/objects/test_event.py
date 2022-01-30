import unittest
import invoiced
from invoiced.test.objects.operations import (
    TestEndpoint,
    RetrievableObject,
    ListAll
)


class TestEvent(TestEndpoint, RetrievableObject,
                ListAll, unittest.TestCase):
    objectClass = invoiced.Event
    endpoint = '/events'
