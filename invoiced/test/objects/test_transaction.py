import unittest
import invoiced
import responses


class TestTransaction(unittest.TestCase):

    def setUp(self):
        self.client = invoiced.Client('api_key')

    def test_endpoint(self):
        transaction = invoiced.Transaction(self.client, 123)
        self.assertEqual('/transactions/123', transaction.endpoint())

    @responses.activate
    def test_create(self):
        responses.add('POST', 'https://api.invoiced.com/transactions',
                      status=201,
                      json={"id": 123, "amount": 100})

        transaction = self.client.Transaction.create(amount=800)

        self.assertIsInstance(transaction, invoiced.Transaction)
        self.assertEqual(transaction.id, 123)
        self.assertEqual(transaction.amount, 100)

    @responses.activate
    def test_retrieve(self):
        responses.add('GET', 'https://api.invoiced.com/transactions/123',
                      status=200,
                      json={"id": "123", "amount": 100})

        transaction = self.client.Transaction.retrieve(123)

        self.assertIsInstance(transaction, invoiced.Transaction)
        self.assertEqual(transaction.id, '123')
        self.assertEqual(transaction.amount, 100)

    def test_update_no_params(self):
        transaction = invoiced.Transaction(self.client, 123)
        self.assertFalse(transaction.save())

    @responses.activate
    def test_update(self):
        responses.add('PATCH', 'https://api.invoiced.com/transactions/123',
                      status=200,
                      json={"id": 123, "amount": 100, "sent": True})

        transaction = invoiced.Transaction(self.client, 123)
        transaction.sent = True
        self.assertTrue(transaction.save())

        self.assertTrue(transaction.sent)

    @responses.activate
    def test_list(self):
        responses.add('GET', 'https://api.invoiced.com/transactions',
                      status=200,
                      json=[{"id": 123, "amount": 100}],
                      adding_headers={
                        'x-total-count': '15',
                        'link': '<https://api.invoiced.com/transactions?per_page=25&page=1>; rel="self", <https://api.invoiced.com/transactions?per_page=25&page=1>; rel="first", <https://api.invoiced.com/transactions?per_page=25&page=1>; rel="last"'})  # noqa

        transactions, metadata = self.client.Transaction.list()

        self.assertIsInstance(transactions, list)
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0].id, 123)

        self.assertIsInstance(metadata, invoiced.List)
        self.assertEqual(metadata.total_count, 15)

    @responses.activate
    def test_delete(self):
        responses.add('DELETE', 'https://api.invoiced.com/transactions/123',
                      status=204)

        transaction = invoiced.Transaction(self.client, 123)
        self.assertTrue(transaction.delete())

    @responses.activate
    def test_send(self):
        responses.add('POST',
                      'https://api.invoiced.com/transactions/123/emails',
                      status=201,
                      json=[{"id": 4567, "email": "test@example.com"}])

        transaction = invoiced.Transaction(self.client, 123)
        emails = transaction.send()

        self.assertEqual(type(emails), list)
        self.assertEqual(len(emails), 1)
        self.assertIsInstance(emails[0], invoiced.Email)
        self.assertEqual(emails[0].id, 4567)

    @responses.activate
    def test_refund(self):
        responses.add('POST',
                      'https://api.invoiced.com/transactions/123/refunds',
                      status=201,
                      json={"id": 456})

        transaction = invoiced.Transaction(self.client, 123)
        refund = transaction.refund(amount=800)

        self.assertIsInstance(refund, invoiced.Transaction)
        self.assertEqual(refund.id, 456)

    @responses.activate
    def test_initiate_charge(self):
        responses.add('POST',
                      'https://api.invoiced.com/charges',
                      status=201,
                      json={"id": "a1b2c3", "amount": 100,
                            "object": "charge"})

        transaction = self.client.Transaction.initiate_charge(amount=100,
                                                              payment_source_type="card") # noqa

        self.assertIsInstance(transaction, invoiced.Transaction)
        self.assertEqual(transaction.id, "a1b2c3")
        self.assertEqual(transaction.object, "charge")
