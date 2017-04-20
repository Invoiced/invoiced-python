import unittest
import invoiced
import responses


class TestPlan(unittest.TestCase):

    def setUp(self):
        self.client = invoiced.Client('api_key')

    def test_endpoint(self):
        plan = invoiced.Plan(self.client, "starter")
        self.assertEqual('/plans/starter', plan.endpoint())

    @responses.activate
    def test_create(self):
        responses.add('POST', 'https://api.invoiced.com/plans',
                      status=201,
                      json={"id": "starter", "name": "Starter"})

        plan = self.client.Plan.create(id="starter")

        self.assertIsInstance(plan, invoiced.Plan)
        self.assertEqual(plan.id, "starter")
        self.assertEqual(plan.name, "Starter")

    @responses.activate
    def test_retrieve(self):
        responses.add('GET', 'https://api.invoiced.com/plans/starter',
                      status=200,
                      json={"id": "starter", "name": "Starter"})

        plan = self.client.Plan.retrieve("starter")

        self.assertIsInstance(plan, invoiced.Plan)
        self.assertEqual(plan.id, "starter")
        self.assertEqual(plan.name, "Starter")

    def test_update_no_params(self):
        plan = invoiced.Plan(self.client, "starter")
        self.assertFalse(plan.save())

    @responses.activate
    def test_update(self):
        responses.add('PATCH', 'https://api.invoiced.com/plans/starter',
                      status=200,
                      json={"id": "starter", "name": "Pro"})

        plan = invoiced.Plan(self.client, "starter")
        plan.name = "Pro"
        self.assertTrue(plan.save())

        self.assertEqual(plan.name, "Pro")

    @responses.activate
    def test_list(self):
        responses.add('GET', 'https://api.invoiced.com/plans',
                      status=200,
                      json=[{"id": "starter", "name": "Pro"}],
                      adding_headers={
                        'x-total-count': '15',
                        'link': '<https://api.invoiced.com/plans?per_page=25&page=1>; rel="self", <https://api.invoiced.com/plans?per_page=25&page=1>; rel="first", <https://api.invoiced.com/plans?per_page=25&page=1>; rel="last"'})  # noqa

        plans, metadata = self.client.Plan.list()

        self.assertIsInstance(plans, list)
        self.assertEqual(len(plans), 1)
        self.assertEqual(plans[0].id, "starter")

        self.assertIsInstance(metadata, invoiced.List)
        self.assertEqual(metadata.total_count, 15)

    @responses.activate
    def test_delete(self):
        responses.add('DELETE', 'https://api.invoiced.com/plans/starter',
                      status=200,
                      json={"id": "starter", "name": "Pro"})

        plan = invoiced.Plan(self.client, "starter")
        self.assertTrue(plan.delete())
        self.assertEquals(plan.name, "Pro")
