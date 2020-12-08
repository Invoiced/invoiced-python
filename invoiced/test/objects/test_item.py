import unittest
import invoiced
import responses


class TestItem(unittest.TestCase):

    def setUp(self):
        self.client = invoiced.Client('api_key')

    def test_endpoint(self):
        item = invoiced.Item(self.client, "paper")
        self.assertEqual('/items/paper', item.endpoint())

    @responses.activate
    def test_create(self):
        responses.add('POST', 'https://api.invoiced.com/items',
                      status=201,
                      json={"id": "paper", "name": "Paper"})

        item = self.client.Item.create(id="paper")

        self.assertIsInstance(item, invoiced.Item)
        self.assertEqual(item.id, "paper")
        self.assertEqual(item.name, "Paper")

    @responses.activate
    def test_retrieve(self):
        responses.add('GET', 'https://api.invoiced.com/items/paper',
                      status=200,
                      json={"id": "paper", "name": "Paper"})

        item = self.client.Item.retrieve("paper")

        self.assertIsInstance(item, invoiced.Item)
        self.assertEqual(item.id, "paper")
        self.assertEqual(item.name, "Paper")

    def test_update_no_params(self):
        item = invoiced.Item(self.client, "paper")
        self.assertFalse(item.save())

    @responses.activate
    def test_update(self):
        responses.add('PATCH', 'https://api.invoiced.com/items/paper',
                      status=200,
                      json={"id": "paper", "name": "More Paper"})

        item = invoiced.Item(self.client, "paper")
        item.name = "More Paper"
        self.assertTrue(item.save())

        self.assertEqual(item.name, "More Paper")

    @responses.activate
    def test_list(self):
        responses.add('GET', 'https://api.invoiced.com/items',
                      status=200,
                      json=[{"id": "paper", "name": "More Paper"}],
                      adding_headers={
                        'x-total-count': '15',
                        'link': '<https://api.invoiced.com/items?per_page=25&page=1>; rel="self", <https://api.invoiced.com/items?per_page=25&page=1>; rel="first", <https://api.invoiced.com/items?per_page=25&page=1>; rel="last"'})  # noqa

        items, metadata = self.client.Item.list()

        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].id, "paper")

        self.assertIsInstance(metadata, invoiced.List)
        self.assertEqual(metadata.total_count, 15)

    @responses.activate
    def test_delete(self):
        responses.add('DELETE', 'https://api.invoiced.com/items/paper',
                      status=200,
                      json={"id": "paper", "name": "More Paper"})

        item = invoiced.Item(self.client, "paper")
        self.assertTrue(item.delete())
        self.assertEqual(item.name, "More Paper")
