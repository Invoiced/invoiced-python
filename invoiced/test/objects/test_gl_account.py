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


class TestGlAccount(TestEndpoint, CreatableObject, RetrievableObject,
                    UpdatableObject, DeletableObject, ListAll,
                    unittest.TestCase):
    objectClass = invoiced.GlAccount
    endpoint = '/gl_accounts'
