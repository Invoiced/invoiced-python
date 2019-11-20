import unittest
import invoiced
import responses


class TestPaymentSource(unittest.TestCase):

    def setUp(self):
        self.client = invoiced.Client('api_key')

    @responses.activate
    def test_endpoint(self):
        responses.add('POST', 'https://api.invoiced.com/customers/1234/payment_sources',
                      status=201,
                      json={"id": 123})

        customer = invoiced.Customer(self.client, 1234)
        source = customer.payment_sources().create()
        self.assertEqual('/customers/1234/payment_sources/123', source.endpoint())

    @responses.activate
    def test_create(self):
        responses.add('POST', 'https://api.invoiced.com/customers/1234/payment_sources',
                      status=201,
                      json={"id": 123, "object": "card"})

        customer = invoiced.Customer(self.client, 1234)
        source = customer.payment_sources().create(method="card")

        self.assertIsInstance(source, invoiced.PaymentSource)
        self.assertEqual(source.id, 123)
        self.assertEqual(source.object, "card")

    @responses.activate
    def test_list(self):
        responses.add('GET', 'https://api.invoiced.com/customers/1234/payment_sources',
                      status=200,
                      json=[{"id": 123, "object": "card"}],
                      adding_headers={
                        'x-total-count': '15',
                        'link': '<https://api.invoiced.com/payment_sources?per_page=25&page=1>; rel="self", <https://api.invoiced.com/payment_sources?per_page=25&page=1>; rel="first", <https://api.invoiced.com/contacts?per_page=25&page=1>; rel="last"'})  # noqa

        customer = invoiced.Customer(self.client, 1234)
        sources, metadata = customer.payment_sources().list()

        self.assertIsInstance(sources, list)
        self.assertEqual(len(sources), 1)
        self.assertEqual(sources[0].id, 123)

        self.assertIsInstance(metadata, invoiced.List)
        self.assertEqual(metadata.total_count, 15)

    @responses.activate
    def test_delete(self):
        responses.add('POST', 'https://api.invoiced.com/customers/1234/payment_sources',
                      status=201,
                      json={"id": 123, "object": "card"})

        responses.add('DELETE', 'https://api.invoiced.com/customers/1234/cards/123',
                      status=204)

        customer = invoiced.Customer(self.client, 1234)
        source = customer.payment_sources().create()

        self.assertTrue(source.delete())
