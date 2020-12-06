import unittest
import invoiced
import responses


class TestTask(unittest.TestCase):

    def setUp(self):
        self.client = invoiced.Client('api_key')

    def test_endpoint(self):
        task = invoiced.Task(self.client, 123)
        self.assertEqual('/tasks/123', task.endpoint())

    @responses.activate
    def test_create(self):
        responses.add('POST', 'https://api.invoiced.com/tasks',
                      status=201,
                      json={"id": 123, "user_id": 234, "customer_id": 345,
                            "name": "1st Call", "action": "phone",
                            "due_date": 1234567890})

        task = invoiced.Task(self.client)
        task = task.create(customer_id=345, user_id=234, name="1st Call",
                           action="phone", due_date=1234567890)

        self.assertIsInstance(task, invoiced.Task)
        self.assertEqual(task.id, 123)
        self.assertEqual(task.customer_id, 345)
        self.assertEqual(task.name, "1st Call")

    @responses.activate
    def test_retrieve(self):
        responses.add('GET', 'https://api.invoiced.com/tasks/123',
                      status=200,
                      json={"id": 123, "user_id": 234, "customer_id": 345,
                            "name": "1st Call", "action": "phone",
                            "due_date": 1234567890})

        task = invoiced.Task(self.client)
        task = task.retrieve(123)

        self.assertIsInstance(task, invoiced.Task)
        self.assertEqual(task.id, 123)
        self.assertEqual(task.action, "phone")

    def test_update_no_params(self):
        task = invoiced.Task(self.client, 123)
        self.assertFalse(task.save())

    @responses.activate
    def test_update(self):
        responses.add('PATCH', 'https://api.invoiced.com/tasks/123',
                      status=200,
                      json={"id": 123, "user_id": 234, "customer_id": 345,
                            "name": "2nd Call", "action": "phone",
                            "due_date": 1234567890})

        task = invoiced.Task(self.client, 123)
        task.name = "2nd Call"
        self.assertTrue(task.save())

        self.assertEqual(task.name, "2nd Call")

    @responses.activate
    def test_list(self):
        responses.add('GET', 'https://api.invoiced.com/tasks',
                      status=200,
                      json=[{"id": 123, "user_id": 234, "customer_id": 345,
                             "name": "2nd Call", "action": "phone",
                             "due_date": 1234567890}],
                      adding_headers={
                        'x-total-count': '15',
                        'link': '<https://api.invoiced.com/tasks?per_page=25&page=1>; rel="self", <https://api.invoiced.com/tasks?per_page=25&page=1>; rel="first", <https://api.invoiced.com/tasks?per_page=25&page=1>; rel="last"'})  # noqa

        task = invoiced.Task(self.client)
        tasks, metadata = task.list()

        self.assertIsInstance(tasks, list)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].id, 123)

        self.assertIsInstance(metadata, invoiced.List)
        self.assertEqual(metadata.total_count, 15)

    @responses.activate
    def test_delete(self):
        responses.add('DELETE', 'https://api.invoiced.com/tasks/123',
                      status=204)

        task = invoiced.Task(self.client, 123)
        self.assertTrue(task.delete())
