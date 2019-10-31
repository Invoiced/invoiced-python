import unittest
import invoiced
import responses


class TestNote(unittest.TestCase):

    def setUp(self):
        self.client = invoiced.Client('api_key')

    def test_endpoint(self):
        note = invoiced.Note(self.client, 123)
        self.assertEqual('/notes/123', note.endpoint())

    @responses.activate
    def test_create(self):
        responses.add('POST', 'https://api.invoiced.com/notes',
                      status=201,
                      json={"id": 123, "customer": 234, "notes": "Contents of note"})

        note = invoiced.Note(self.client)
        note = note.create(customer_id=234, notes="Contents of note")

        self.assertIsInstance(note, invoiced.Note)
        self.assertEqual(note.id, 123)
        self.assertEqual(note.customer, 234)
        self.assertEqual(note.notes, "Contents of note")

    @responses.activate
    def test_retrieve(self):
        responses.add('GET', 'https://api.invoiced.com/notes/123',
                      status=200,
                      json={"id": 123, "customer": 234, "notes": "Contents of note"})

        note = invoiced.Note(self.client)
        note = note.retrieve(123)

        self.assertIsInstance(note, invoiced.Note)
        self.assertEqual(note.id, 123)
        self.assertEqual(note.notes, "Contents of note")

    def test_update_no_params(self):
        note = invoiced.Note(self.client, 123)
        self.assertFalse(note.save())

    @responses.activate
    def test_update(self):
        responses.add('PATCH', 'https://api.invoiced.com/notes/123',
                      status=200,
                      json={"id": 123, "customer": 234, "notes": "600"})

        note = invoiced.Note(self.client, 123)
        note.notes = "600"
        self.assertTrue(note.save())

        self.assertEqual(note.notes, "600")

    @responses.activate
    def test_list(self):
        responses.add('GET', 'https://api.invoiced.com/notes',
                      status=200,
                      json=[{"id": 123, "customer": 234, "notes": "Contents of note"}],
                      adding_headers={
                        'x-total-count': '15',
                        'link': '<https://api.invoiced.com/notes?per_page=25&page=1>; rel="self", <https://api.invoiced.com/notes?per_page=25&page=1>; rel="first", <https://api.invoiced.com/notes?per_page=25&page=1>; rel="last"'})  # noqa

        note = invoiced.Note(self.client)
        notes, metadata = note.list()

        self.assertIsInstance(notes, list)
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0].id, 123)

        self.assertIsInstance(metadata, invoiced.List)
        self.assertEqual(metadata.total_count, 15)

    @responses.activate
    def test_delete(self):
        responses.add('DELETE', 'https://api.invoiced.com/notes/123',
                      status=204)

        note = invoiced.Note(self.client, 123)
        self.assertTrue(note.delete())