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


class TestSmsTemplate(TestEndpoint, CreatableObject, RetrievableObject,
                      UpdatableObject, DeletableObject, ListAll,
                      unittest.TestCase):
    objectClass = invoiced.SmsTemplate
    endpoint = '/sms_templates'
