import unittest
import invoiced
from invoiced import util


class TestUtil(unittest.TestCase):

    def setUp(self):
        self.client = invoiced.Client('api_key')

    def test_convert_to_object(self):
        customer = {'id': 100}
        obj = util.convert_to_object(self.client.Customer, customer)

        self.assertIsInstance(obj, invoiced.Customer)
        self.assertEqual(obj.id, 100)

    def test_build_objects(self):
        customers = [
            {'id': 100},
            {'id': 101}
        ]

        objects = util.build_objects(self.client.Customer, customers)
        self.assertEqual(2, len(objects))
        self.assertIsInstance(objects[0], invoiced.Customer)
        self.assertIsInstance(objects[1], invoiced.Customer)
        self.assertEqual(objects[0].id, 100)
        self.assertEqual(objects[1].id, 101)

    def test_uri_encode(self):
        params = {
            "test": "property",
            "filter": {
                "levels": "work",
                "nesting": {
                    "works": True
                }
            },
            "array": [
                "should",
                {"also": True},
                ["work"]
            ]
        }

        encoded = util.uri_encode(params)
        self.assertEqual(encoded, "array[]=should&array[][also]=True&array[]=work&filter[levels]=work&filter[nesting][works]=True&test=property")  # noqa

if __name__ == '__main__':
    unittest.main()
