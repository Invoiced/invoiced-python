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


class TestEmailTemplate(TestEndpoint, CreatableObject, RetrievableObject,
                        UpdatableObject, DeletableObject, ListAll,
                        unittest.TestCase):
    objectClass = invoiced.EmailTemplate
    endpoint = '/email_templates'
