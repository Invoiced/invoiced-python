import unittest
import invoiced
import responses


class TestCreditBalanceAdjustment(unittest.TestCase):

    def setUp(self):
        self.client = invoiced.Client('api_key')

    def test_endpoint(self):
        creditBalanceAdjustment = invoiced.CreditBalanceAdjustment(
            self.client, 123)
        self.assertEqual('/credit_balance_adjustments/123',
                         creditBalanceAdjustment.endpoint())

    @responses.activate
    def test_create(self):
        responses.add('POST',
                      'https://api.invoiced.com/credit_balance_adjustments',
                      status=201,
                      json={"id": 123, "name": "Alpha"})

        creditBalanceAdjustment = invoiced.CreditBalanceAdjustment(self.client)
        creditBalanceAdjustment = creditBalanceAdjustment.create(name="Alpha")

        self.assertIsInstance(creditBalanceAdjustment,
                              invoiced.CreditBalanceAdjustment)
        self.assertEqual(creditBalanceAdjustment.id, 123)
        self.assertEqual(creditBalanceAdjustment.name, "Alpha")

    @responses.activate
    def test_retrieve(self):
        responses.add('GET',
                      'https://api.invoiced.com/credit_balance_adjustments/123', # noqa
                      status=200,
                      json={"id": "123", "name": "Alpha"})

        creditBalanceAdjustment = invoiced.CreditBalanceAdjustment(
            self.client)
        creditBalanceAdjustment = creditBalanceAdjustment.retrieve(123)

        self.assertIsInstance(creditBalanceAdjustment,
                              invoiced.CreditBalanceAdjustment)
        self.assertEqual(creditBalanceAdjustment.id, '123')
        self.assertEqual(creditBalanceAdjustment.name, "Alpha")

    def test_update_no_params(self):
        creditBalanceAdjustment = invoiced.CreditBalanceAdjustment(
            self.client, 123)
        self.assertFalse(creditBalanceAdjustment.save())

    @responses.activate
    def test_update(self):
        responses.add('PATCH',
                      'https://api.invoiced.com/credit_balance_adjustments/123', # noqa
                      status=200,
                      json={"id": 123, "name": 600})

        creditBalanceAdjustment = invoiced.CreditBalanceAdjustment(
            self.client, 123)
        creditBalanceAdjustment.name = 600
        self.assertTrue(creditBalanceAdjustment.save())

        self.assertTrue(creditBalanceAdjustment.name)

    @responses.activate
    def test_list(self):
        responses.add('GET',
                      'https://api.invoiced.com/credit_balance_adjustments',
                      status=200,
                      json=[{"id": 123, "name": "Alpha"}],
                      adding_headers={
                        'x-total-count': '10',
                        'link': '<https://api.invoiced.com/credit_balance_adjustments?per_page=25&page=1>; rel="self", <https://api.invoiced.com/credit_balance_adjustments?per_page=25&page=1>; rel="first", <https://api.invoiced.com/credit_balance_adjustments?per_page=25&page=1>; rel="last"'})  # noqa

        creditBalanceAdjustment = invoiced.CreditBalanceAdjustment(
            self.client)
        creditBalanceAdjustments, metadata = creditBalanceAdjustment.list()

        self.assertIsInstance(creditBalanceAdjustments, list)
        self.assertEqual(len(creditBalanceAdjustments), 1)
        self.assertEqual(creditBalanceAdjustments[0].id, 123)

        self.assertIsInstance(metadata, invoiced.List)
        self.assertEqual(metadata.total_count, 10)

    @responses.activate
    def test_delete(self):
        responses.add('DELETE',
                      'https://api.invoiced.com/credit_balance_adjustments/123', # noqa
                      status=204)

        creditBalanceAdjustment = invoiced.CreditBalanceAdjustment(
            self.client, 123)
        self.assertTrue(creditBalanceAdjustment.delete())
