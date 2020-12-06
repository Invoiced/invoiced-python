import unittest
import invoiced
import responses


class TestRefund(unittest.TestCase):

    def setUp(self):
        self.client = invoiced.Client('api_key')

    def test_endpoint(self):
        refund = invoiced.Refund(self.client, 123)
        self.assertEqual('/refunds/123', refund.endpoint())

    @responses.activate
    def test_create(self):
        responses.add('POST',
                      'https://api.invoiced.com/charges/123/refunds',
                      status=201,
                      json={"id": 456})

        refund = self.client.Refund.create(123, amount=800)

        self.assertIsInstance(refund, invoiced.Refund)
        self.assertEqual(refund.id, 456)
