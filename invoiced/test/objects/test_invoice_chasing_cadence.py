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


class TestInvoiceChasingCadence(TestEndpoint, CreatableObject,
                                RetrievableObject, UpdatableObject,
                                DeletableObject, ListAll, unittest.TestCase):
    objectClass = invoiced.InvoiceChasingCadence
    endpoint = '/invoice_chasing_cadences'
