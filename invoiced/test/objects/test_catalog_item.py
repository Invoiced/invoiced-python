import unittest
import invoiced
import responses


class TestCatalogItem(unittest.TestCase):

    def setUp(self):
        self.client = invoiced.Client('api_key')

    def test_endpoint(self):
        catalog_item = invoiced.CatalogItem(self.client, "paper")
        self.assertEqual('/catalog_items/paper', catalog_item.endpoint())

    @responses.activate
    def test_create(self):
        responses.add('POST', 'https://api.invoiced.com/catalog_items',
                      status=201,
                      json={"id": "paper", "name": "Paper"})

        catalog_item = self.client.CatalogItem.create(id="paper")

        self.assertIsInstance(catalog_item, invoiced.CatalogItem)
        self.assertEqual(catalog_item.id, "paper")
        self.assertEqual(catalog_item.name, "Paper")

    @responses.activate
    def test_retrieve(self):
        responses.add('GET', 'https://api.invoiced.com/catalog_items/paper',
                      status=200,
                      json={"id": "paper", "name": "Paper"})

        catalog_item = self.client.CatalogItem.retrieve("paper")

        self.assertIsInstance(catalog_item, invoiced.CatalogItem)
        self.assertEqual(catalog_item.id, "paper")
        self.assertEqual(catalog_item.name, "Paper")

    def test_update_no_params(self):
        catalog_item = invoiced.CatalogItem(self.client, "paper")
        self.assertFalse(catalog_item.save())

    @responses.activate
    def test_update(self):
        responses.add('PATCH', 'https://api.invoiced.com/catalog_items/paper',
                      status=200,
                      json={"id": "paper", "name": "More Paper"})

        catalog_item = invoiced.CatalogItem(self.client, "paper")
        catalog_item.name = "More Paper"
        self.assertTrue(catalog_item.save())

        self.assertEqual(catalog_item.name, "More Paper")

    @responses.activate
    def test_list(self):
        responses.add('GET', 'https://api.invoiced.com/catalog_items',
                      status=200,
                      json=[{"id": "paper", "name": "More Paper"}],
                      adding_headers={
                        'x-total-count': '15',
                        'link': '<https://api.invoiced.com/catalog_items?per_page=25&page=1>; rel="self", <https://api.invoiced.com/catalog_items?per_page=25&page=1>; rel="first", <https://api.invoiced.com/catalog_items?per_page=25&page=1>; rel="last"'})  # noqa

        catalog_items, metadata = self.client.CatalogItem.list()

        self.assertIsInstance(catalog_items, list)
        self.assertEqual(len(catalog_items), 1)
        self.assertEqual(catalog_items[0].id, "paper")

        self.assertIsInstance(metadata, invoiced.List)
        self.assertEqual(metadata.total_count, 15)

    @responses.activate
    def test_delete(self):
        responses.add('DELETE', 'https://api.invoiced.com/catalog_items/paper',
                      status=200,
                      json={"id": "paper", "name": "More Paper"})

        catalog_item = invoiced.CatalogItem(self.client, "paper")
        self.assertTrue(catalog_item.delete())
        self.assertEquals(catalog_item.name, "More Paper")
