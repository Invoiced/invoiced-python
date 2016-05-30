import unittest
import invoiced
import responses


class TestInvoice(unittest.TestCase):

    def setUp(self):
        self.client = invoiced.Client('api_key')

    def test_endpoint(self):
        invoice = invoiced.Invoice(self.client, 123)
        self.assertEqual('/invoices/123', invoice.endpoint())

    @responses.activate
    def test_create(self):
        responses.add('POST', 'https://api.invoiced.com/invoices',
                      status=201,
                      json={"id": 123, "number": "INV-0001"})

        invoice = self.client.Invoice.create(number='INV-0001')

        self.assertIsInstance(invoice, invoiced.Invoice)
        self.assertEqual(invoice.id, 123)
        self.assertEqual(invoice.number, 'INV-0001')

    @responses.activate
    def test_retrieve(self):
        responses.add('GET', 'https://api.invoiced.com/invoices/123',
                      status=200,
                      json={"id": "123", "number": "INV-0001"})

        invoice = self.client.Invoice.retrieve(123)

        self.assertIsInstance(invoice, invoiced.Invoice)
        self.assertEqual(invoice.id, '123')
        self.assertEqual(invoice.number, 'INV-0001')

    def test_update_no_params(self):
        invoice = invoiced.Invoice(self.client, 123)
        self.assertFalse(invoice.save())

    @responses.activate
    def test_update(self):
        responses.add('PATCH', 'https://api.invoiced.com/invoices/123',
                      status=200,
                      json={"id": 123, "closed": True})

        invoice = invoiced.Invoice(self.client, 123)
        invoice.closed = True
        self.assertTrue(invoice.save())

        self.assertTrue(invoice.closed)

    @responses.activate
    def test_list(self):
        responses.add('GET', 'https://api.invoiced.com/invoices',
                      status=200,
                      json=[{"id": 123, "number": "INV-0001"}],
                      adding_headers={
                        'x-total-count': '15',
                        'link': '<https://api.invoiced.com/invoices?per_page=25&page=1>; rel="self", <https://api.invoiced.com/invoices?per_page=25&page=1>; rel="first", <https://api.invoiced.com/invoices?per_page=25&page=1>; rel="last"'})  # noqa

        invoices, metadata = self.client.Invoice.list()

        self.assertIsInstance(invoices, list)
        self.assertEqual(len(invoices), 1)
        self.assertEqual(invoices[0].id, 123)

        self.assertIsInstance(metadata, invoiced.List)
        self.assertEqual(metadata.total_count, 15)

    @responses.activate
    def test_delete(self):
        responses.add('DELETE', 'https://api.invoiced.com/invoices/123',
                      status=204)

        invoice = invoiced.Invoice(self.client, 123)
        self.assertTrue(invoice.delete())

    @responses.activate
    def test_send(self):
        responses.add('POST', 'https://api.invoiced.com/invoices/123/emails',
                      status=201,
                      json=[{"id": 4567, "email": "test@example.com"}])

        invoice = invoiced.Invoice(self.client, 123)
        emails = invoice.send()

        self.assertEqual(type(emails), list)
        self.assertEqual(len(emails), 1)
        self.assertIsInstance(emails[0], invoiced.Email)
        self.assertEqual(emails[0].id, 4567)

    @responses.activate
    def test_pay(self):
        responses.add('POST', 'https://api.invoiced.com/invoices/123/pay',
                      status=200,
                      json={"paid": True})

        invoice = invoiced.Invoice(self.client, 123)
        self.assertTrue(invoice.pay())

        self.assertTrue(invoice.paid)

    @responses.activate
    def test_attachments(self):
        responses.add('GET',
                      'https://api.invoiced.com/invoices/123/attachments',
                      status=200,
                      json=[{"file": {"id": 456}}],
                      adding_headers={
                        'x-total-count': '10',
                        'link': '<https://api.invoiced.com/invoices/123/attachments?per_page=25&page=1>; rel="self", <https://api.invoiced.com/invoices/123/attachments?per_page=25&page=1>; rel="first", <https://api.invoiced.com/invoices/123/attachments?per_page=25&page=1>; rel="last"'})  # noqa

        invoice = invoiced.Invoice(self.client, 123)
        attachments, metadata = invoice.attachments()

        self.assertIsInstance(attachments, list)
        self.assertEqual(len(attachments), 1)
        self.assertEqual(attachments[0].id, 456)

        self.assertIsInstance(metadata, invoiced.List)
        self.assertEqual(metadata.total_count, 10)
