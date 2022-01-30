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


class TestCustomer(TestEndpoint, CreatableObject, RetrievableObject,
                   UpdatableObject, DeletableObject, ListAll,
                   unittest.TestCase):
    objectClass = invoiced.Customer
    endpoint = '/customers'

    def setUp(self):
        self.client = invoiced.Client('api_key')

    @responses.activate
    def test_send_statement(self):
        responses.add('POST', 'https://api.invoiced.com/customers/123/emails',
                      status=201,
                      json=[{"id": 4567, "email": "test@example.com"}])

        customer = invoiced.Customer(self.client, 123)
        emails = customer.send_statement()

        self.assertEqual(type(emails), list)
        self.assertEqual(len(emails), 1)
        self.assertIsInstance(emails[0], invoiced.Email)
        self.assertEqual(emails[0].id, 4567)

    @responses.activate
    def test_send_statement_sms(self):
        responses.add('POST',
                      'https://api.invoiced.com/customers/123/text_messages', # noqa
                      status=201,
                      json=[{"id": 890, "message": "example"}])

        customer = invoiced.Customer(self.client, 123)
        text_messages = customer.send_statement_sms(message="example")

        self.assertEqual(type(text_messages), list)
        self.assertEqual(len(text_messages), 1)
        self.assertIsInstance(text_messages[0], invoiced.TextMessage)
        self.assertEqual(text_messages[0].id, 890)

    @responses.activate
    def test_send_statement_letter(self):
        responses.add('POST', 'https://api.invoiced.com/customers/123/letters',
                      status=201,
                      json=[{"id": 891, "state": "queued"}])

        customer = invoiced.Customer(self.client, 123)
        letters = customer.send_statement_letter()

        self.assertEqual(type(letters), list)
        self.assertEqual(len(letters), 1)
        self.assertIsInstance(letters[0], invoiced.Letter)
        self.assertEqual(letters[0].id, 891)

    @responses.activate
    def test_balance(self):
        responses.add('GET',
                      'https://api.invoiced.com/customers/123/balance',
                      status=200,
                      json={"total_outstanding": 1000, "available_credits": 0, "past_due": True})  # noqa

        customer = invoiced.Customer(self.client, 123)
        balance = customer.balance()

        expected = {
            'past_due': True,
            'available_credits': 0,
            'total_outstanding': 1000
        }

        self.assertEqual(balance, expected)

    @responses.activate
    def test_create_contact(self):
        responses.add('POST',
                      'https://api.invoiced.com/customers/123/contacts',
                      status=201,
                      json={"id": 456, "name": "Nancy"})

        customer = invoiced.Customer(self.client, 123)
        contact = customer.contacts().create(name="Nancy")

        self.assertIsInstance(contact, invoiced.Contact)
        self.assertEqual(contact.id, 456)
        self.assertEqual(contact.name, "Nancy")

    @responses.activate
    def test_retrieve_contact(self):
        responses.add('GET',
                      'https://api.invoiced.com/customers/123/contacts/456',
                      status=200,
                      json={"id": "456", "name": "Nancy"})

        customer = invoiced.Customer(self.client, 123)
        contact = customer.contacts().retrieve(456)

        self.assertIsInstance(contact, invoiced.Contact)
        self.assertEqual(contact.id, '456')
        self.assertEqual(contact.name, "Nancy")

    @responses.activate
    def test_list_contacts(self):
        responses.add('GET',
                      'https://api.invoiced.com/customers/123/contacts',
                      status=200,
                      json=[{"id": 456, "name": "Nancy"}],
                      adding_headers={
                        'x-total-count': '10',
                        'link': '<https://api.invoiced.com/customers/123/contacts?per_page=25&page=1>; rel="self", <https://api.invoiced.com/customers/123/contacts?per_page=25&page=1>; rel="first", <https://api.invoiced.com/customers/123/contacts?per_page=25&page=1>; rel="last"'})  # noqa

        customer = invoiced.Customer(self.client, 123)
        contacts, metadata = customer.contacts().list()

        self.assertIsInstance(contacts, list)
        self.assertEqual(len(contacts), 1)
        self.assertEqual(contacts[0].id, 456)

        self.assertIsInstance(metadata, invoiced.List)
        self.assertEqual(metadata.total_count, 10)

    @responses.activate
    def test_create_note(self):
        responses.add('POST',
                      'https://api.invoiced.com/customers/123/notes',
                      status=201,
                      json={"id": 567, "notes": "Text of note"})

        customer = invoiced.Customer(self.client, 123)
        note = customer.list_notes().create(customer_id=123,
                                            notes="Text of note")

        self.assertIsInstance(note, invoiced.Note)
        self.assertEqual(note.id, 567)
        self.assertEqual(note.notes, "Text of note")

    @responses.activate
    def test_retrieve_note(self):
        responses.add('GET',
                      'https://api.invoiced.com/customers/123/notes/567',
                      status=200,
                      json={"id": 567, "notes": "Text of note"})

        customer = invoiced.Customer(self.client, 123)
        note = customer.list_notes().retrieve(567)

        self.assertIsInstance(note, invoiced.Note)
        self.assertEqual(note.id, 567)
        self.assertEqual(note.notes, "Text of note")

    @responses.activate
    def test_list_notes(self):
        responses.add('GET',
                      'https://api.invoiced.com/customers/123/notes',
                      status=200,
                      json=[{"id": 567, "notes": "Text of note"}],
                      adding_headers={
                        'x-total-count': '10',
                        'link': '<https://api.invoiced.com/customers/123/notes?per_page=25&page=1>; rel="self", <https://api.invoiced.com/customers/123/notes?per_page=25&page=1>; rel="first", <https://api.invoiced.com/customers/123/notes?per_page=25&page=1>; rel="last"'})  # noqa

        customer = invoiced.Customer(self.client, 123)
        notes, metadata = customer.list_notes().list()

        self.assertIsInstance(notes, list)
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0].id, 567)

        self.assertIsInstance(metadata, invoiced.List)
        self.assertEqual(metadata.total_count, 10)

    @responses.activate
    def test_create_pending_line_item(self):
        responses.add('POST',
                      'https://api.invoiced.com/customers/123/line_items',
                      status=201,
                      json={"id": 456, "unit_cost": 500})

        customer = invoiced.Customer(self.client, 123)
        line_item = customer.line_items().create(unit_cost=500)

        self.assertIsInstance(line_item, invoiced.LineItem)
        self.assertEqual(line_item.id, 456)
        self.assertEqual(line_item.unit_cost, 500)

    @responses.activate
    def test_retrieve_pending_line_item(self):
        responses.add('GET',
                      'https://api.invoiced.com/customers/123/line_items/456',
                      status=200,
                      json={"id": "456", "unit_cost": 500})

        customer = invoiced.Customer(self.client, 123)
        line_item = customer.line_items().retrieve(456)

        self.assertIsInstance(line_item, invoiced.LineItem)
        self.assertEqual(line_item.id, '456')
        self.assertEqual(line_item.unit_cost, 500)

    @responses.activate
    def test_list_pending_line_items(self):
        responses.add('GET',
                      'https://api.invoiced.com/customers/123/line_items',
                      status=200,
                      json=[{"id": 456, "unit_cost": 500}],
                      adding_headers={
                        'x-total-count': '10',
                        'link': '<https://api.invoiced.com/customers/123/line_items?per_page=25&page=1>; rel="self", <https://api.invoiced.com/customers/123/line_items?per_page=25&page=1>; rel="first", <https://api.invoiced.com/customers/123/line_items?per_page=25&page=1>; rel="last"'})  # noqa

        customer = invoiced.Customer(self.client, 123)
        line_items, metadata = customer.line_items().list()

        self.assertIsInstance(line_items, list)
        self.assertEqual(len(line_items), 1)
        self.assertEqual(line_items[0].id, 456)

        self.assertIsInstance(metadata, invoiced.List)
        self.assertEqual(metadata.total_count, 10)

    @responses.activate
    def test_invoice(self):
        responses.add('POST',
                      'https://api.invoiced.com/customers/123/invoices',
                      status=201,
                      json={"id": 456, "total": 500})

        customer = invoiced.Customer(self.client, 123)
        invoice = customer.invoice()

        self.assertIsInstance(invoice, invoiced.Invoice)
        self.assertEqual(invoice.id, 456)
        self.assertEqual(invoice.total, 500)

    @responses.activate
    def test_consolidate_invoices(self):
        responses.add('POST',
                      'https://api.invoiced.com/customers/123/consolidate_invoices', # noqa
                      status=201,
                      json={"id": 123456, "total": 567890})

        customer = invoiced.Customer(self.client, 123)
        invoice = customer.consolidate_invoices()

        self.assertIsInstance(invoice, invoiced.Invoice)
        self.assertEqual(invoice.id, 123456)
        self.assertEqual(invoice.total, 567890)
