import unittest
import responses
import invoiced
from invoiced.test.objects.operations import (
    TestEndpoint,
    CreatableObject,
    RetrievableObject,
    UpdatableObject,
    DeletableObject,
    ListAll
)


class TestCreditNote(TestEndpoint, CreatableObject, RetrievableObject,
                     UpdatableObject, DeletableObject, ListAll,
                     unittest.TestCase):
    objectClass = invoiced.CreditNote
    endpoint = '/credit_notes'

    def setUp(self):
        self.client = invoiced.Client('api_key')

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
