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
    def test_send_sms(self):
        responses.add('POST', 'https://api.invoiced.com/invoices/123/text_messages',
                      status=201,
                      json=[{"id": 9876, "message": "example"}])

        invoice = invoiced.Invoice(self.client, 123)
        text_messages = invoice.send_sms(message="example")

        self.assertEqual(type(text_messages), list)
        self.assertEqual(len(text_messages), 1)
        self.assertIsInstance(text_messages[0], invoiced.TextMessage)
        self.assertEqual(text_messages[0].id, 9876)

    @responses.activate
    def test_send_letter(self):
        responses.add('POST', 'https://api.invoiced.com/invoices/123/letters',
                      status=201,
                      json=[{"id": 8765, "state": "queued"}])

        invoice = invoiced.Invoice(self.client, 123)
        letters = invoice.send_letter()

        self.assertEqual(type(letters), list)
        self.assertEqual(len(letters), 1)
        self.assertIsInstance(letters[0], invoiced.Letter)
        self.assertEqual(letters[0].id, 8765)

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

    @responses.activate
    def test_create_note(self):
        responses.add('POST',
                      'https://api.invoiced.com/invoices/123/notes',
                      status=201,
                      json={"id": 567, "notes": "Text of note"})

        invoice = invoiced.Invoice(self.client, 123)
        note = invoice.notes().create(invoice_id=123, notes="Text of note")

        self.assertIsInstance(note, invoiced.Note)
        self.assertEqual(note.id, 567)
        self.assertEqual(note.notes, "Text of note")

    @responses.activate
    def test_retrieve_note(self):
        responses.add('GET',
                      'https://api.invoiced.com/invoices/123/notes/567',
                      status=200,
                      json={"id": 567, "notes": "Text of note"})

        invoice = invoiced.Invoice(self.client, 123)
        note = invoice.notes().retrieve(567)

        self.assertIsInstance(note, invoiced.Note)
        self.assertEqual(note.id, 567)
        self.assertEqual(note.notes, "Text of note")

    @responses.activate
    def test_list_notes(self):
        responses.add('GET',
                      'https://api.invoiced.com/invoices/123/notes',
                      status=200,
                      json=[{"id": 567, "notes": "Text of note"}],
                      adding_headers={
                        'x-total-count': '10',
                        'link': '<https://api.invoiced.com/invoices/123/notes?per_page=25&page=1>; rel="self", <https://api.invoiced.com/invoices/123/notes?per_page=25&page=1>; rel="first", <https://api.invoiced.com/invoices/123/notes?per_page=25&page=1>; rel="last"'})  # noqa

        invoice = invoiced.Invoice(self.client, 123)
        notes, metadata = invoice.notes().list()

        self.assertIsInstance(notes, list)
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0].id, 567)

        self.assertIsInstance(metadata, invoiced.List)
        self.assertEqual(metadata.total_count, 10)


    @responses.activate
    def test_create_payment_plan(self):
        responses.add('PUT',
                      'https://api.invoiced.com/invoices/123/payment_plan',
                      status=201,
                      json={"id": 456, "status": "active"})

        invoice = invoiced.Invoice(self.client, 123)
        payment_plan = invoice.payment_plan().create(installments=[{
            'date': 1234, 'amount': 100}])

        self.assertIsInstance(payment_plan, invoiced.PaymentPlan)
        self.assertEqual(payment_plan.id, 456)
        self.assertEqual(payment_plan.status, "active")

    @responses.activate
    def test_retrieve_payment_plan(self):
        responses.add('GET',
                      'https://api.invoiced.com/invoices/123/payment_plan',
                      status=200,
                      json={"id": "456", "status": "active"})

        invoice = invoiced.Invoice(self.client, 123)
        payment_plan = invoice.payment_plan().retrieve()

        self.assertIsInstance(payment_plan, invoiced.PaymentPlan)
        self.assertEqual(payment_plan.id, '456')
        self.assertEqual(payment_plan.status, "active")

    @responses.activate
    def test_void(self):
        responses.add('POST', 'https://api.invoiced.com/invoices/123/void',
                      status=200,
                      json={"id": 123, "status": 'voided'})

        invoice = invoiced.Invoice(self.client, 123)
        invoice.void()

        self.assertIsInstance(invoice, invoiced.Invoice)
        self.assertEqual(invoice.status, 'voided')