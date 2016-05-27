import unittest
import invoiced
import responses


class TestContact(unittest.TestCase):

    def setUp(self):
        self.client = invoiced.Client('api_key')

    def test_endpoint(self):
        contact = invoiced.Contact(self.client, 123)
        self.assertEqual('/contacts/123', contact.endpoint())

    @responses.activate
    def test_create(self):
        responses.add('POST', 'https://api.invoiced.com/contacts',
                      status=201,
                      json={"id": 123, "name": "Nancy"})

        contact = invoiced.Contact(self.client)
        contact = contact.create(name="Nancy")

        self.assertIsInstance(contact, invoiced.Contact)
        self.assertEqual(contact.id, 123)
        self.assertEqual(contact.name, "Nancy")

    @responses.activate
    def test_retrieve(self):
        responses.add('GET', 'https://api.invoiced.com/contacts/123',
                      status=200,
                      json={"id": "123", "name": "Nancy"})

        contact = invoiced.Contact(self.client)
        contact = contact.retrieve(123)

        self.assertIsInstance(contact, invoiced.Contact)
        self.assertEqual(contact.id, '123')
        self.assertEqual(contact.name, "Nancy")

    def test_update_no_params(self):
        contact = invoiced.Contact(self.client, 123)
        self.assertFalse(contact.save())

    @responses.activate
    def test_update(self):
        responses.add('PATCH', 'https://api.invoiced.com/contacts/123',
                      status=200,
                      json={"id": 123, "name": 600})

        contact = invoiced.Contact(self.client, 123)
        contact.name = 600
        self.assertTrue(contact.save())

        self.assertTrue(contact.name)

    @responses.activate
    def test_list(self):
        responses.add('GET', 'https://api.invoiced.com/contacts',
                      status=200,
                      json=[{"id": 123, "name": "Nancy"}],
                      adding_headers={
                        'x-total-count': '15',
                        'link': '<https://api.invoiced.com/contacts?per_page=25&page=1>; rel="self", <https://api.invoiced.com/contacts?per_page=25&page=1>; rel="first", <https://api.invoiced.com/contacts?per_page=25&page=1>; rel="last"'})  # noqa

        contact = invoiced.Contact(self.client)
        contacts, metadata = contact.list()

        self.assertIsInstance(contacts, list)
        self.assertEqual(len(contacts), 1)
        self.assertEqual(contacts[0].id, 123)

        self.assertIsInstance(metadata, invoiced.List)
        self.assertEqual(metadata.total_count, 15)

    @responses.activate
    def test_delete(self):
        responses.add('DELETE', 'https://api.invoiced.com/contacts/123',
                      status=204)

        contact = invoiced.Contact(self.client, 123)
        self.assertTrue(contact.delete())
