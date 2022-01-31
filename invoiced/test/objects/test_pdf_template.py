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


class TestPdfTemplate(TestEndpoint, CreatableObject, RetrievableObject,
                      UpdatableObject, DeletableObject, ListAll,
                      unittest.TestCase):
    objectClass = invoiced.PdfTemplate
    endpoint = '/pdf_templates'
