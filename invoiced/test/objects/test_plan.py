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


class TestPlan(TestEndpoint, CreatableObject, RetrievableObject,
               UpdatableObject, DeletableObject, ListAll,
               unittest.TestCase):
    objectClass = invoiced.Plan
    endpoint = '/plans'
