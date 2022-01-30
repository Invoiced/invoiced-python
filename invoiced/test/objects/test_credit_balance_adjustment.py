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


class TestCreditBalanceAdjustment(TestEndpoint, CreatableObject,
                                  RetrievableObject, UpdatableObject,
                                  DeletableObject, ListAll, unittest.TestCase):
    objectClass = invoiced.CreditBalanceAdjustment
    endpoint = '/credit_balance_adjustments'
