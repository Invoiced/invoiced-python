import unittest
import invoiced
import responses


class TestPayment(unittest.TestCase):

    def setUp(self):
        self.client = invoiced.Client('api_key')

    def test_endpoint(self):
        payment = invoiced.Payment(self.client, 123)
        self.assertEqual('/payments/123', payment.endpoint())

    @responses.activate
    def test_create(self):
        responses.add('POST', 'https://api.invoiced.com/payments',
                      status=201,
                      json={"id": 123, "amount": 100})

        payment = self.client.Payment.create(amount=800)

        self.assertIsInstance(payment, invoiced.Payment)
        self.assertEqual(payment.id, 123)
        self.assertEqual(payment.amount, 100)

    @responses.activate
    def test_retrieve(self):
        responses.add('GET', 'https://api.invoiced.com/payments/123',
                      status=200,
                      json={"id": "123", "amount": 100})

        payment = self.client.Payment.retrieve(123)

        self.assertIsInstance(payment, invoiced.Payment)
        self.assertEqual(payment.id, '123')
        self.assertEqual(payment.amount, 100)

    def test_update_no_params(self):
        payment = invoiced.Payment(self.client, 123)
        self.assertFalse(payment.save())

    @responses.activate
    def test_update(self):
        responses.add('PATCH', 'https://api.invoiced.com/payments/123',
                      status=200,
                      json={"id": 123, "amount": 100, "sent": True})

        payment = invoiced.Payment(self.client, 123)
        payment.sent = True
        self.assertTrue(payment.save())

        self.assertTrue(payment.sent)

    @responses.activate
    def test_list(self):
        responses.add('GET', 'https://api.invoiced.com/payments',
                      status=200,
                      json=[{"id": 123, "amount": 100}],
                      adding_headers={
                        'x-total-count': '15',
                        'link': '<https://api.invoiced.com/payments?per_page=25&page=1>; rel="self", <https://api.invoiced.com/payments?per_page=25&page=1>; rel="first", <https://api.invoiced.com/payments?per_page=25&page=1>; rel="last"'})  # noqa

        payments, metadata = self.client.Payment.list()

        self.assertIsInstance(payments, list)
        self.assertEqual(len(payments), 1)
        self.assertEqual(payments[0].id, 123)

        self.assertIsInstance(metadata, invoiced.List)
        self.assertEqual(metadata.total_count, 15)

    @responses.activate
    def test_delete(self):
        responses.add('DELETE', 'https://api.invoiced.com/payments/123',
                      status=204)

        payment = invoiced.Payment(self.client, 123)
        self.assertTrue(payment.delete())

    @responses.activate
    def test_send(self):
        responses.add('POST',
                      'https://api.invoiced.com/payments/123/emails',
                      status=201,
                      json=[{"id": 4567, "email": "test@example.com"}])

        payment = invoiced.Payment(self.client, 123)
        emails = payment.send()

        self.assertEqual(type(emails), list)
        self.assertEqual(len(emails), 1)
        self.assertIsInstance(emails[0], invoiced.Email)
        self.assertEqual(emails[0].id, 4567)
