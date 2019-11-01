import unittest
import invoiced
import responses


class TestTaxRate(unittest.TestCase):

    def setUp(self):
        self.client = invoiced.Client('api_key')

    def test_endpoint(self):
        tax_rate = invoiced.TaxRate(self.client, "vat")
        self.assertEqual('/tax_rates/vat', tax_rate.endpoint())

    @responses.activate
    def test_create(self):
        responses.add('POST', 'https://api.invoiced.com/tax_rates',
                      status=201,
                      json={"id": "vat", "name": "Tax"})

        tax_rate = self.client.TaxRate.create(id="vat")

        self.assertIsInstance(tax_rate, invoiced.TaxRate)
        self.assertEqual(tax_rate.id, "vat")
        self.assertEqual(tax_rate.name, "Tax")

    @responses.activate
    def test_retrieve(self):
        responses.add('GET', 'https://api.invoiced.com/tax_rates/vat',
                      status=200,
                      json={"id": "vat", "name": "Tax"})

        tax_rate = self.client.TaxRate.retrieve("vat")

        self.assertIsInstance(tax_rate, invoiced.TaxRate)
        self.assertEqual(tax_rate.id, "vat")
        self.assertEqual(tax_rate.name, "Tax")

    def test_update_no_params(self):
        tax_rate = invoiced.TaxRate(self.client, "vat")
        self.assertFalse(tax_rate.save())

    @responses.activate
    def test_update(self):
        responses.add('PATCH', 'https://api.invoiced.com/tax_rates/vat',
                      status=200,
                      json={"id": "vat", "name": "VAT"})

        tax_rate = invoiced.TaxRate(self.client, "vat")
        tax_rate.name = "VAT"
        self.assertTrue(tax_rate.save())

        self.assertEqual(tax_rate.name, "VAT")

    @responses.activate
    def test_list(self):
        responses.add('GET', 'https://api.invoiced.com/tax_rates',
                      status=200,
                      json=[{"id": "vat", "name": "VAT"}],
                      adding_headers={
                        'x-total-count': '15',
                        'link': '<https://api.invoiced.com/tax_rates?per_page=25&page=1>; rel="self", <https://api.invoiced.com/tax_rates?per_page=25&page=1>; rel="first", <https://api.invoiced.com/tax_rates?per_page=25&page=1>; rel="last"'})  # noqa

        tax_rates, metadata = self.client.TaxRate.list()

        self.assertIsInstance(tax_rates, list)
        self.assertEqual(len(tax_rates), 1)
        self.assertEqual(tax_rates[0].id, "vat")

        self.assertIsInstance(metadata, invoiced.List)
        self.assertEqual(metadata.total_count, 15)

    @responses.activate
    def test_delete(self):
        responses.add('DELETE', 'https://api.invoiced.com/tax_rates/vat',
                      status=200,
                      json={"id": "vat", "name": "VAT"})

        tax_rate = invoiced.TaxRate(self.client, "vat")
        self.assertTrue(tax_rate.delete())