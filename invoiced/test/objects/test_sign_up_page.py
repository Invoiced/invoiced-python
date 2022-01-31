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


class TestSignUpPage(TestEndpoint, CreatableObject, RetrievableObject,
                     UpdatableObject, DeletableObject, ListAll,
                     unittest.TestCase):
    objectClass = invoiced.SignUpPage
    endpoint = '/sign_up_pages'
