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


class TestSubscription(TestEndpoint, CreatableObject, RetrievableObject,
                       UpdatableObject, DeletableObject, ListAll,
                       unittest.TestCase):
    objectClass = invoiced.Subscription
    endpoint = '/subscriptions'

    @responses.activate
    def test_preview(self):
        responses.add('POST', 'https://api.invoiced.com/subscriptions/preview',
                      status=200,
                      json={"first_invoice": {"id": False}, "mrr": 9})

        client = invoiced.Client('apikey')
        preview = client.Subscription.preview(customer=1234,
                                              plan="enterprise")
        self.assertEqual(preview['first_invoice'], {'id': False})
