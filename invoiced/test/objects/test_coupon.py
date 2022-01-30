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


class TestCoupon(TestEndpoint, CreatableObject, RetrievableObject,
                 UpdatableObject, DeletableObject, ListAll,
                 unittest.TestCase):
    objectClass = invoiced.Coupon
    endpoint = '/coupons'
