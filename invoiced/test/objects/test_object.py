import unittest
import invoiced
import sys


class TestObject(unittest.TestCase):

    def setUp(self):
        self.client = invoiced.Client('api_key')

    def test_endpoint(self):
        customer = invoiced.Customer(self.client, 123)
        self.assertEqual('/customers/123', customer.endpoint())

        customer.set_endpoint_base('/blah')
        self.assertEqual('/blah', customer.endpoint_base())
        self.assertEqual('/blah/customers/123', customer.endpoint())

    def test_accessors(self):
        customer = invoiced.Customer(self.client, 123, {'name': 'Pied Piper'})

        self.assertEqual(customer.id, 123)
        self.assertEqual(customer.name, 'Pied Piper')
        self.assertEqual(customer['name'], 'Pied Piper')

        customer.name = 'Renamed'
        self.assertEqual(customer.name, 'Renamed')

        customer['name'] = 'Pied Piper'
        self.assertEqual(customer['name'], 'Pied Piper')

        self.assertEqual({'id': 123, 'name': 'Pied Piper'}, dict(customer))

        customer.refresh_from({'id': 123, 'notes': '....'})

        self.assertEqual('....', customer.notes)
        # name attribute should no longer be available
        with self.assertRaises(AttributeError):
            customer.name

        del customer._client

        with self.assertRaises(KeyError):
            del customer.name

        customer['notes'] = '....'
        del customer['notes']
        with self.assertRaises(AttributeError):
            customer.notes

        customer.update({'name': 'Test'})
        self.assertEqual(customer.name, 'Test')

    def test_missing_id(self):
        customer = invoiced.Customer(self.client)

        with self.assertRaises(ValueError):
            customer.retrieve(False)

    def test_cannot_access_private(self):
        customer = invoiced.Customer(self.client)

        with self.assertRaises(AttributeError):
            customer._private

    def test_empty_string_error(self):
        customer = invoiced.Customer(self.client)

        with self.assertRaises(ValueError):
            customer.test = ''

    @unittest.skipIf(sys.version_info < (3, 4), 'inconsistent results between versions')  # noqa
    def test_str(self):
        customer = invoiced.Customer(self.client, 123, {'name': 'Pied Piper'})

        self.assertEqual(customer.__str__(), "{\n  \"id\": 123,\n  \"name\": \"Pied Piper\"\n}")  # noqa
        self.assertEqual(customer.__repr__(), "<Customer id=123 at "+hex(id(customer))+"> JSON: {\n  \"id\": 123,\n  \"name\": \"Pied Piper\"\n}")  # noqa
