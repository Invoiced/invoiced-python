import unittest
import responses
import invoiced


class TestPaymentPlan(unittest.TestCase):

    def setUp(self):
        self.client = invoiced.Client('api_key')

    def test_endpoint(self):
        payment_plan = invoiced.PaymentPlan(self.client, 123)
        self.assertEqual('/payment_plan', payment_plan.endpoint())

    @responses.activate
    def test_create(self):
        responses.add('PUT', 'https://api.invoiced.com/payment_plan',
                      status=201,
                      json={"id": 123, "status": "active"})

        paymentPlan = invoiced.PaymentPlan(self.client)
        payment_plan = paymentPlan.create(installments=[{
            'date': 1234, 'amount': 100}])

        self.assertIsInstance(payment_plan, invoiced.PaymentPlan)
        self.assertEqual(payment_plan.id, 123)
        self.assertEqual(payment_plan.status, "active")

    @responses.activate
    def test_retrieve(self):
        responses.add('GET', 'https://api.invoiced.com/payment_plan',
                      status=200,
                      json={"id": 123, "status": "active"})

        paymentPlan = invoiced.PaymentPlan(self.client)
        payment_plan = paymentPlan.retrieve()

        self.assertIsInstance(payment_plan, invoiced.PaymentPlan)
        self.assertEqual(payment_plan.id, 123)
        self.assertEqual(payment_plan.status, "active")

    @responses.activate
    def test_cancel(self):
        responses.add('DELETE', 'https://api.invoiced.com/payment_plan',
                      status=204)

        payment_plan = invoiced.PaymentPlan(self.client, 123)
        self.assertTrue(payment_plan.cancel())
