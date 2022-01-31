import unittest
import invoiced
from invoiced.test.objects.operations import (
    TestEndpoint,
    ListAll
)


class TestInbox(TestEndpoint, ListAll, unittest.TestCase):
    objectClass = invoiced.Inbox
    endpoint = '/inboxes'
