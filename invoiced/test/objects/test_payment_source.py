import unittest
import invoiced
import responses


class TestPaymentSource(unittest.TestCase):

    def setUp(self):
        self.client = invoiced.Client('api_key')

    @responses.activate
    def test_endpoint_and_create_bank_account(self):
        responses.add('POST',
                      'https://api.invoiced.com/customers/1234/payment_sources', # noqa
                      status=201,
                      json={"id": 123, "object": "bank_account"})

        customer = invoiced.Customer(self.client, 1234)
        source = customer.payment_sources().create()
        # if true, endpoint on creation is correct
        self.assertEqual(123, source.id)
        # if true, endpoint after creation is correct
        self.assertEqual("/customers/1234/bank_accounts/123",
                         source.endpoint())

    @responses.activate
    def test_endpoint_and_create_card(self):
        responses.add('POST',
                      'https://api.invoiced.com/customers/1234/payment_sources', # noqa
                      status=201,
                      json={"id": 456, "object": "card"})

        customer = invoiced.Customer(self.client, 1234)
        source = customer.payment_sources().create()
        # if true, endpoint on creation is correct
        self.assertEqual(456, source.id)
        # if true, endpoint after creation is correct
        self.assertEqual("/customers/1234/cards/456", source.endpoint())

    @responses.activate
    def test_list(self):
        responses.add('GET',
                      'https://api.invoiced.com/customers/1234/payment_sources', # noqa
                      status=200,
                      json=[
                          {"id": 123, "object": "bank_account"},
                          {"id": 456, "object": "card"}],
                      adding_headers={
                        'x-total-count': '15',
                        'link': '<https://api.invoiced.com/payment_sources?per_page=25&page=1>; rel="self", <https://api.invoiced.com/payment_sources?per_page=25&page=1>; rel="first", <https://api.invoiced.com/contacts?per_page=25&page=1>; rel="last"'})  # noqa

        customer = invoiced.Customer(self.client, 1234)
        sources, metadata = customer.payment_sources().list()

        self.assertIsInstance(sources, list)
        self.assertEqual(len(sources), 2)
        self.assertEqual(sources[0].id, 123)
        self.assertIsInstance(sources[0], invoiced.BankAccount)
        self.assertIsInstance(sources[1], invoiced.Card)

        self.assertIsInstance(metadata, invoiced.List)
        self.assertEqual(metadata.total_count, 15)

    @responses.activate
    def test_delete_card(self):
        responses.add('POST',
                      'https://api.invoiced.com/customers/1234/payment_sources', # noqa
                      status=201,
                      json={"id": 123, "object": "card"})

        responses.add('DELETE',
                      'https://api.invoiced.com/customers/1234/cards/123',
                      status=204)

        customer = invoiced.Customer(self.client, 1234)
        source = customer.payment_sources().create()

        self.assertIsInstance(source, invoiced.Card)
        self.assertTrue(source.delete())

    @responses.activate
    def test_delete_bank_account(self):
        responses.add('POST',
                      'https://api.invoiced.com/customers/1234/payment_sources', # noqa
                      status=201,
                      json={"id": 123, "object": "bank_account"})

        responses.add('DELETE',
                      'https://api.invoiced.com/customers/1234/bank_accounts/123', # noqa
                      status=204)

        customer = invoiced.Customer(self.client, 1234)
        source = customer.payment_sources().create()

        self.assertIsInstance(source, invoiced.BankAccount)
        self.assertTrue(source.delete())
