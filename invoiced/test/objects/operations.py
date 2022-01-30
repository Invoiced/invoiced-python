import responses

import invoiced


class TestEndpoint:

    def test_endpoint(self):
        client = invoiced.Client('api_key')
        obj = self.objectClass(client, 123)
        self.assertEqual(self.endpoint + '/123', obj.endpoint())


class CreatableObject:

    @responses.activate
    def test_create(self):
        responses.add('POST', 'https://api.invoiced.com' + self.endpoint,
                      status=201,
                      json={"id": 123})

        client = invoiced.Client('api_key')
        obj = self.objectClass(client).create(name="Nancy")

        self.assertIsInstance(obj, self.objectClass)
        self.assertEqual(obj.id, 123)


class RetrievableObject:

    @responses.activate
    def test_retrieve(self):
        responses.add('GET', 'https://api.invoiced.com' +
                      self.endpoint + '/123',
                      status=200,
                      json={"id": "123"})

        client = invoiced.Client('api_key')
        obj = self.objectClass(client).retrieve(123)

        self.assertIsInstance(obj, self.objectClass)
        self.assertEqual(obj.id, '123')


class UpdatableObject:

    def test_update_no_params(self):
        client = invoiced.Client('api_key')
        obj = self.objectClass(client, 123)
        self.assertFalse(obj.save())

    @responses.activate
    def test_update(self):
        responses.add('PATCH', 'https://api.invoiced.com' +
                      self.endpoint + '/123',
                      status=200,
                      json={"id": 123, "name": "Test"})

        client = invoiced.Client('api_key')
        obj = self.objectClass(client, 123)
        obj.name = "Test"
        self.assertTrue(obj.save())

        self.assertEqual(obj.name, "Test")


class DeletableObject:

    @responses.activate
    def test_delete(self):
        responses.add('DELETE', 'https://api.invoiced.com' +
                      self.endpoint + '/123',
                      status=204)

        client = invoiced.Client('api_key')
        obj = self.objectClass(client, 123)
        self.assertTrue(obj.delete())


class ListAll:

    @responses.activate
    def test_list(self):
        responses.add('GET', 'https://api.invoiced.com' + self.endpoint,
                      status=200,
                      json=[{"id": 123, "name": "Nancy"}],
                      adding_headers={
                        'x-total-count': '15',
                        'link': '<https://api.invoiced.com' +  self.endpoint + '?per_page=25&page=1>; rel="self", <https://api.invoiced.com' +  self.endpoint + '?per_page=25&page=1>; rel="first", <https://api.invoiced.com' +  self.endpoint + '?per_page=25&page=1>; rel="last"'})  # noqa

        client = invoiced.Client('api_key')
        objects, metadata = self.objectClass(client).list()

        self.assertIsInstance(objects, list)
        self.assertEqual(len(objects), 1)
        self.assertEqual(objects[0].id, 123)

        self.assertIsInstance(metadata, invoiced.List)
        self.assertEqual(metadata.total_count, 15)
