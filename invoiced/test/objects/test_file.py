import unittest
import invoiced
import responses


class TestFile(unittest.TestCase):

    def setUp(self):
        self.client = invoiced.Client('api_key')

    def test_endpoint(self):
        file = invoiced.File(self.client, 123)
        self.assertEqual('/files/123', file.endpoint())

    @responses.activate
    def test_create(self):
        responses.add('POST', 'https://api.invoiced.com/files',
                      status=201,
                      json={"id": 123, "name": "Filename"})

        file = invoiced.File(self.client)
        file = file.create(name="Filename")

        self.assertIsInstance(file, invoiced.File)
        self.assertEqual(file.id, 123)
        self.assertEqual(file.name, "Filename")

    @responses.activate
    def test_retrieve(self):
        responses.add('GET', 'https://api.invoiced.com/files/123',
                      status=200,
                      json={"id": "123", "name": "Filename"})

        file = invoiced.File(self.client)
        file = file.retrieve(123)

        self.assertIsInstance(file, invoiced.File)
        self.assertEqual(file.id, '123')
        self.assertEqual(file.name, "Filename")

    @responses.activate
    def test_delete(self):
        responses.add('DELETE', 'https://api.invoiced.com/files/123',
                      status=204)

        file = invoiced.File(self.client, 123)
        self.assertTrue(file.delete())
