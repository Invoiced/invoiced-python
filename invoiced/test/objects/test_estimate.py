import unittest
import invoiced
from invoiced.test.objects.operations import (
    TestEndpoint,
    CreatableObject,
    RetrievableObject,
    UpdatableObject,
    DeletableObject,
    ListAll
)
import responses


class TestEstimate(TestEndpoint, CreatableObject, RetrievableObject,
                   UpdatableObject, DeletableObject, ListAll,
                   unittest.TestCase):
    objectClass = invoiced.Estimate
    endpoint = '/estimates'

    def setUp(self):
        self.client = invoiced.Client('api_key')

    @responses.activate
    def test_send(self):
        responses.add('POST',
                      'https://api.invoiced.com/estimates/123/emails',
                      status=201,
                      json=[{"id": 4567, "email": "test@example.com"}])

        estimate = invoiced.Estimate(self.client, 123)
        emails = estimate.send()

        self.assertEqual(type(emails), list)
        self.assertEqual(len(emails), 1)
        self.assertIsInstance(emails[0], invoiced.Email)
        self.assertEqual(emails[0].id, 4567)

    @responses.activate
    def test_attachments(self):
        responses.add('GET',
                      'https://api.invoiced.com/estimates/123/attachments',
                      status=200,
                      json=[{"file": {"id": 456}}],
                      adding_headers={
                        'x-total-count': '10',
                        'link': '<https://api.invoiced.com/estimates/123/attachments?per_page=25&page=1>; rel="self", <https://api.invoiced.com/estimates/123/attachments?per_page=25&page=1>; rel="first", <https://api.invoiced.com/estimates/123/attachments?per_page=25&page=1>; rel="last"'})  # noqa

        estimate = invoiced.Estimate(self.client, 123)
        attachments, metadata = estimate.attachments()

        self.assertIsInstance(attachments, list)
        self.assertEqual(len(attachments), 1)
        self.assertEqual(attachments[0].id, 456)

        self.assertIsInstance(metadata, invoiced.List)
        self.assertEqual(metadata.total_count, 10)

    @responses.activate
    def test_invoice(self):
        responses.add('POST',
                      'https://api.invoiced.com/estimates/123/invoice',
                      status=201,
                      json={"id": 456, "total": 500})

        estimate = invoiced.Estimate(self.client, 123)
        invoice = estimate.invoice()

        self.assertIsInstance(invoice, invoiced.Invoice)
        self.assertEqual(invoice.id, 456)
        self.assertEqual(invoice.total, 500)

    @responses.activate
    def test_void(self):
        responses.add('POST', 'https://api.invoiced.com/estimates/123/void',
                      status=200,
                      json={"id": 123, "status": 'voided'})

        estimate = invoiced.Estimate(self.client, 123)
        estimate.void()

        self.assertIsInstance(estimate, invoiced.Estimate)
        self.assertEqual(estimate.status, 'voided')
