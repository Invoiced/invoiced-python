import unittest
import responses
import invoiced
from invoiced.test.objects.operations import (
    TestEndpoint,
    CreatableObject,
    RetrievableObject,
    UpdatableObject,
    DeletableObject,
    ListAll
)


class TestPayment(TestEndpoint, CreatableObject, RetrievableObject,
                  UpdatableObject, DeletableObject, ListAll,
                  unittest.TestCase):
    objectClass = invoiced.Payment
    endpoint = '/payments'

    @responses.activate
    def test_send(self):
        responses.add('POST',
                      'https://api.invoiced.com/payments/123/emails',
                      status=201,
                      json=[{"id": 4567, "email": "test@example.com"}])

        client = invoiced.Client('apikey')
        payment = invoiced.Payment(client, 123)
        emails = payment.send()

        self.assertEqual(type(emails), list)
        self.assertEqual(len(emails), 1)
        self.assertIsInstance(emails[0], invoiced.Email)
        self.assertEqual(emails[0].id, 4567)
