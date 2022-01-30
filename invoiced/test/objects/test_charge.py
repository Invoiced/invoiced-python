import unittest

import responses

import invoiced


class TestCharge(unittest.TestCase):

    def setUp(self):
        self.client = invoiced.Client('api_key')

    def test_endpoint(self):
        charge = invoiced.Charge(self.client, 123)
        self.assertEqual('/charges/123', charge.endpoint())

    @responses.activate
    def test_create(self):
        responses.add('POST',
                      'https://api.invoiced.com/charges',
                      status=201,
                      json={"id": "a1b2c3",
                            "amount": 100,
                            "object": "payment"})

        payment = self.client.Charge.create(amount=100,
                                            payment_source_type="card")

        self.assertIsInstance(payment, invoiced.Payment)
        self.assertEqual(payment.id, "a1b2c3")
        self.assertEqual(payment.object, "payment")
