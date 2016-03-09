import unittest
import invoiced
import responses


class TestSubscription(unittest.TestCase):

    def setUp(self):
        self.client = invoiced.Client('api_key')

    def test_endpoint(self):
        subscription = invoiced.Subscription(self.client, 123)
        self.assertEquals('/subscriptions/123', subscription.endpoint())

    @responses.activate
    def test_create(self):
        responses.add('POST', 'https://api.invoiced.com/subscriptions',
                      status=201,
                      json={"id": 123, "plan": "starter"})

        subscription = self.client.Subscription.create(customer=456)

        self.assertIsInstance(subscription, invoiced.Subscription)
        self.assertEqual(subscription.id, 123)
        self.assertEqual(subscription.plan, "starter")

    @responses.activate
    def test_retrieve(self):
        responses.add('GET', 'https://api.invoiced.com/subscriptions/123',
                      status=200,
                      json={"id": "123", "plan": "starter"})

        subscription = self.client.Subscription.retrieve(123)

        self.assertIsInstance(subscription, invoiced.Subscription)
        self.assertEqual(subscription.id, '123')
        self.assertEqual(subscription.plan, "starter")

    def test_update_no_params(self):
        subscription = invoiced.Subscription(self.client, 123)
        self.assertFalse(subscription.save())

    @responses.activate
    def test_update(self):
        responses.add('PATCH', 'https://api.invoiced.com/subscriptions/123',
                      status=200,
                      json={"id": 123, "plan": "pro"})

        subscription = invoiced.Subscription(self.client, 123)
        subscription.plan = "pro"
        self.assertTrue(subscription.save())

        self.assertEqual(subscription.plan, "pro")

    @responses.activate
    def test_list(self):
        responses.add('GET', 'https://api.invoiced.com/subscriptions',
                      status=200,
                      json=[{"id": 123, "plan": "pro"}],
                      adding_headers={
                        'x-total-count': '15',
                        'link': '<https://api.invoiced.com/subscriptions?per_page=25&page=1>; rel="self", <https://api.invoiced.com/subscriptions?per_page=25&page=1>; rel="first", <https://api.invoiced.com/subscriptions?per_page=25&page=1>; rel="last"'})  # noqa

        subscriptions, metadata = self.client.Subscription.list()

        self.assertIsInstance(subscriptions, list)
        self.assertEqual(len(subscriptions), 1)
        self.assertEqual(subscriptions[0].id, 123)

        self.assertIsInstance(metadata, invoiced.List)
        self.assertEqual(metadata.total_count, 15)

    @responses.activate
    def test_cancel(self):
        responses.add('DELETE', 'https://api.invoiced.com/subscriptions/123',
                      status=204)

        subscription = invoiced.Subscription(self.client, 123)
        self.assertTrue(subscription.cancel())
