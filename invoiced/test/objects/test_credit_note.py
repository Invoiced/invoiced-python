import unittest
import invoiced
import responses


class TestCreditNote(unittest.TestCase):

    def setUp(self):
        self.client = invoiced.Client('api_key')

    def test_endpoint(self):
        creditNote = invoiced.CreditNote(self.client, 123)
        self.assertEqual('/credit_notes/123', creditNote.endpoint())

    @responses.activate
    def test_create(self):
        responses.add('POST', 'https://api.invoiced.com/credit_notes',
                      status=201,
                      json={"id": 123, "number": "CN-0001"})

        creditNote = self.client.CreditNote.create(number='CN-0001')

        self.assertIsInstance(creditNote, invoiced.CreditNote)
        self.assertEqual(creditNote.id, 123)
        self.assertEqual(creditNote.number, 'CN-0001')

    @responses.activate
    def test_retrieve(self):
        responses.add('GET', 'https://api.invoiced.com/credit_notes/123',
                      status=200,
                      json={"id": "123", "number": "CN-0001"})

        creditNote = self.client.CreditNote.retrieve(123)

        self.assertIsInstance(creditNote, invoiced.CreditNote)
        self.assertEqual(creditNote.id, '123')
        self.assertEqual(creditNote.number, 'CN-0001')

    def test_update_no_params(self):
        creditNote = invoiced.CreditNote(self.client, 123)
        self.assertFalse(creditNote.save())

    @responses.activate
    def test_update(self):
        responses.add('PATCH', 'https://api.invoiced.com/credit_notes/123',
                      status=200,
                      json={"id": 123, "closed": True})

        creditNote = invoiced.CreditNote(self.client, 123)
        creditNote.closed = True
        self.assertTrue(creditNote.save())

        self.assertTrue(creditNote.closed)

    @responses.activate
    def test_list(self):
        responses.add('GET', 'https://api.invoiced.com/credit_notes',
                      status=200,
                      json=[{"id": 123, "number": "CN-0001"}],
                      adding_headers={
                        'x-total-count': '15',
                        'link': '<https://api.invoiced.com/credit_notes?per_page=25&page=1>; rel="self", <https://api.invoiced.com/credit_notes?per_page=25&page=1>; rel="first", <https://api.invoiced.com/credit_notes?per_page=25&page=1>; rel="last"'})  # noqa

        creditNotes, metadata = self.client.CreditNote.list()

        self.assertIsInstance(creditNotes, list)
        self.assertEqual(len(creditNotes), 1)
        self.assertEqual(creditNotes[0].id, 123)

        self.assertIsInstance(metadata, invoiced.List)
        self.assertEqual(metadata.total_count, 15)

    @responses.activate
    def test_delete(self):
        responses.add('DELETE', 'https://api.invoiced.com/credit_notes/123',
                      status=204)

        creditNote = invoiced.CreditNote(self.client, 123)
        self.assertTrue(creditNote.delete())

    @responses.activate
    def test_send(self):
        responses.add('POST',
                      'https://api.invoiced.com/credit_notes/123/emails',
                      status=201,
                      json=[{"id": 4567, "email": "test@example.com"}])

        creditNote = invoiced.CreditNote(self.client, 123)
        emails = creditNote.send()

        self.assertEqual(type(emails), list)
        self.assertEqual(len(emails), 1)
        self.assertIsInstance(emails[0], invoiced.Email)
        self.assertEqual(emails[0].id, 4567)

    @responses.activate
    def test_attachments(self):
        responses.add('GET',
                      'https://api.invoiced.com/credit_notes/123/attachments',
                      status=200,
                      json=[{"file": {"id": 456}}],
                      adding_headers={
                        'x-total-count': '10',
                        'link': '<https://api.invoiced.com/credit_notes/123/attachments?per_page=25&page=1>; rel="self", <https://api.invoiced.com/credit_notes/123/attachments?per_page=25&page=1>; rel="first", <https://api.invoiced.com/credit_notes/123/attachments?per_page=25&page=1>; rel="last"'})  # noqa

        creditNote = invoiced.CreditNote(self.client, 123)
        attachments, metadata = creditNote.attachments()

        self.assertIsInstance(attachments, list)
        self.assertEqual(len(attachments), 1)
        self.assertEqual(attachments[0].id, 456)

        self.assertIsInstance(metadata, invoiced.List)
        self.assertEqual(metadata.total_count, 10)

    @responses.activate
    def test_void(self):
        responses.add('POST', 'https://api.invoiced.com/credit_notes/123/void',
                      status=200,
                      json={"id": 123, "status": 'voided'})

        credit_note = invoiced.CreditNote(self.client, 123)
        credit_note.void()

        self.assertIsInstance(credit_note, invoiced.CreditNote)
        self.assertEqual(credit_note.status, 'voided')