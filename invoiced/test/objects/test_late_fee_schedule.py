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


class TestLateFeeSchedule(TestEndpoint, CreatableObject, RetrievableObject,
                          UpdatableObject, DeletableObject, ListAll,
                          unittest.TestCase):
    objectClass = invoiced.LateFeeSchedule
    endpoint = '/late_fee_schedules'
