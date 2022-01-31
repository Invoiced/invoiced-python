import unittest
import invoiced
from invoiced.test.objects.operations import (
    TestEndpoint,
    RetrievableObject,
    UpdatableObject,
    ListAll
)


class TestPaymentMethod(TestEndpoint, RetrievableObject,
                        UpdatableObject, ListAll,
                        unittest.TestCase):
    objectClass = invoiced.PaymentMethod
    endpoint = '/payment_methods'
