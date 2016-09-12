import unittest
import invoiced
import responses


class TestEvent(unittest.TestCase):

    def setUp(self):
        self.client = invoiced.Client('api_key')

    def test_endpoint(self):
        event = invoiced.Event(self.client, 123)
        self.assertEqual('/events/123', event.endpoint())

    @responses.activate
    def test_retrieve(self):
        responses.add('GET', 'https://api.invoiced.com/events/123',
                      status=200,
                      json={"id": "123", "type": "customer.created"})

        event = self.client.Event.retrieve(123)

        self.assertIsInstance(event, invoiced.Event)
        self.assertEqual(event.id, '123')
        self.assertEqual(event.type, 'customer.created')

    @responses.activate
    def test_list(self):
        responses.add('GET', 'https://api.invoiced.com/events',
                      status=200,
                      json=[{"id": 123, "type": "customer.created"}],
                      adding_headers={
                        'x-total-count': '15',
                        'link': '<https://api.invoiced.com/events?per_page=25&page=1>; rel="self", <https://api.invoiced.com/events?per_page=25&page=1>; rel="first", <https://api.invoiced.com/events?per_page=25&page=1>; rel="last"'})  # noqa

        events, metadata = self.client.Event.list()

        self.assertIsInstance(events, list)
        self.assertEqual(len(events), 1)
        self.assertIsInstance(events[0], invoiced.Event)
        self.assertEqual(events[0].id, 123)

        self.assertIsInstance(metadata, invoiced.List)
        self.assertEqual(metadata.total_count, 15)
