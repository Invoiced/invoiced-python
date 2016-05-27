import unittest
import invoiced
import responses


class TestLineItem(unittest.TestCase):

    def setUp(self):
        self.client = invoiced.Client('api_key')

    def test_endpoint(self):
        line_item = invoiced.LineItem(self.client, 123)
        self.assertEqual('/line_items/123', line_item.endpoint())

    @responses.activate
    def test_create(self):
        responses.add('POST', 'https://api.invoiced.com/line_items',
                      status=201,
                      json={"id": 123, "amount": 500})

        line = invoiced.LineItem(self.client)
        line_item = line.create(amount=500)

        self.assertIsInstance(line_item, invoiced.LineItem)
        self.assertEqual(line_item.id, 123)
        self.assertEqual(line_item.amount, 500)

    @responses.activate
    def test_retrieve(self):
        responses.add('GET', 'https://api.invoiced.com/line_items/123',
                      status=200,
                      json={"id": "123", "amount": 500})

        line = invoiced.LineItem(self.client)
        line_item = line.retrieve(123)

        self.assertIsInstance(line_item, invoiced.LineItem)
        self.assertEqual(line_item.id, '123')
        self.assertEqual(line_item.amount, 500)

    def test_update_no_params(self):
        line_item = invoiced.LineItem(self.client, 123)
        self.assertFalse(line_item.save())

    @responses.activate
    def test_update(self):
        responses.add('PATCH', 'https://api.invoiced.com/line_items/123',
                      status=200,
                      json={"id": 123, "amount": 600})

        line_item = invoiced.LineItem(self.client, 123)
        line_item.amount = 600
        self.assertTrue(line_item.save())

        self.assertTrue(line_item.amount)

    @responses.activate
    def test_list(self):
        responses.add('GET', 'https://api.invoiced.com/line_items',
                      status=200,
                      json=[{"id": 123, "amount": 500}],
                      adding_headers={
                        'x-total-count': '15',
                        'link': '<https://api.invoiced.com/line_items?per_page=25&page=1>; rel="self", <https://api.invoiced.com/line_items?per_page=25&page=1>; rel="first", <https://api.invoiced.com/line_items?per_page=25&page=1>; rel="last"'})  # noqa

        line = invoiced.LineItem(self.client)
        line_items, metadata = line.list()

        self.assertIsInstance(line_items, list)
        self.assertEqual(len(line_items), 1)
        self.assertEqual(line_items[0].id, 123)

        self.assertIsInstance(metadata, invoiced.List)
        self.assertEqual(metadata.total_count, 15)

    @responses.activate
    def test_delete(self):
        responses.add('DELETE', 'https://api.invoiced.com/line_items/123',
                      status=204)

        line_item = invoiced.LineItem(self.client, 123)
        self.assertTrue(line_item.delete())
