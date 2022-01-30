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


class TestTaxRate(TestEndpoint, CreatableObject, RetrievableObject,
                  UpdatableObject, DeletableObject, ListAll,
                  unittest.TestCase):
    objectClass = invoiced.TaxRate
    endpoint = '/tax_rates'
