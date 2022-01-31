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


class TestCustomerChasingCadence(TestEndpoint, CreatableObject,
                                 RetrievableObject, UpdatableObject,
                                 DeletableObject, ListAll, unittest.TestCase):
    objectClass = invoiced.CustomerChasingCadence
    endpoint = '/customer_chasing_cadences'
