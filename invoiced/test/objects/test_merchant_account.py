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


class TestMerchantAccount(TestEndpoint, CreatableObject, RetrievableObject,
                          UpdatableObject, DeletableObject, ListAll,
                          unittest.TestCase):
    objectClass = invoiced.MerchantAccount
    endpoint = '/merchant_accounts'
