from invoiced.operations import (
    InvoicedObject,
    CreateableObject,
    DeleteableObject,
    ListableObject,
    UpdateableObject,
    List)
from invoiced import util


class Attachment(InvoicedObject):
    pass


class CreditNote(CreateableObject, DeleteableObject, ListableObject,
                 UpdateableObject):

    def send(self, **opts):
        endpoint = self.endpoint()+"/emails"
        response = self._client.request('POST', endpoint, opts)

        # build email objects
        email = Email(self._client)
        return util.build_objects(email, response['body'])

    def attachments(self, **opts):
        response = self._client.request('GET',
                                        self.endpoint()+"/attachments",
                                        opts)

        # ensure each attachment has an ID
        body = response['body']
        for attachment in body:
            if 'id' not in attachment:
                attachment['id'] = attachment['file']['id']

        # build attachment objects
        attachment = Attachment(self._client)
        attachments = util.build_objects(attachment, body)

        # store the metadata from the list operation
        metadata = List(response['headers']['link'],
                        response['headers']['x-total-count'])

        return attachments, metadata


class Customer(CreateableObject, DeleteableObject, ListableObject,
               UpdateableObject):

    def send_statement(self, **opts):
        endpoint = self.endpoint()+"/emails"
        response = self._client.request('POST', endpoint, opts)

        # build email objects
        email = Email(self._client)
        return util.build_objects(email, response['body'])

    def balance(self):
        endpoint = self.endpoint()+"/balance"
        response = self._client.request('GET', endpoint)

        return response['body']

    def contacts(self):
        contact = Contact(self._client)
        contact.set_endpoint_base(self.endpoint())

        return contact

    def line_items(self):
        line = LineItem(self._client)
        line.set_endpoint_base(self.endpoint())

        return line

    def invoice(self, **opts):
        endpoint = self.endpoint()+"/invoices"
        response = self._client.request('POST', endpoint, opts)

        # build invoice object
        invoice = Invoice(self._client)
        return util.convert_to_object(invoice, response['body'])


class Contact(CreateableObject, DeleteableObject, ListableObject,
              UpdateableObject):
    pass


class Email(InvoicedObject):
    pass


class Estimate(CreateableObject, DeleteableObject, ListableObject,
               UpdateableObject):

    def send(self, **opts):
        endpoint = self.endpoint()+"/emails"
        response = self._client.request('POST', endpoint, opts)

        # build email objects
        email = Email(self._client)
        return util.build_objects(email, response['body'])

    def attachments(self, **opts):
        response = self._client.request('GET',
                                        self.endpoint()+"/attachments",
                                        opts)

        # ensure each attachment has an ID
        body = response['body']
        for attachment in body:
            if 'id' not in attachment:
                attachment['id'] = attachment['file']['id']

        # build attachment objects
        attachment = Attachment(self._client)
        attachments = util.build_objects(attachment, body)

        # store the metadata from the list operation
        metadata = List(response['headers']['link'],
                        response['headers']['x-total-count'])

        return attachments, metadata

    def invoice(self, **opts):
        endpoint = self.endpoint()+"/invoice"
        response = self._client.request('POST', endpoint, opts)

        # build invoice object
        invoice = Invoice(self._client)
        return util.convert_to_object(invoice, response['body'])


class Event(ListableObject):
    pass


class File(CreateableObject, DeleteableObject):
    pass


class Invoice(CreateableObject, DeleteableObject, ListableObject,
              UpdateableObject):

    def send(self, **opts):
        endpoint = self.endpoint()+"/emails"
        response = self._client.request('POST', endpoint, opts)

        # build email objects
        email = Email(self._client)
        return util.build_objects(email, response['body'])

    def pay(self):
        endpoint = self.endpoint()+"/pay"
        response = self._client.request('POST', endpoint)

        # update the local values with the response
        self.refresh_from(response['body'])

        return response['code'] == 200

    def attachments(self, **opts):
        response = self._client.request('GET',
                                        self.endpoint()+"/attachments",
                                        opts)

        # ensure each attachment has an ID
        body = response['body']
        for attachment in body:
            if 'id' not in attachment:
                attachment['id'] = attachment['file']['id']

        # build attachment objects
        attachment = Attachment(self._client)
        attachments = util.build_objects(attachment, body)

        # store the metadata from the list operation
        metadata = List(response['headers']['link'],
                        response['headers']['x-total-count'])

        return attachments, metadata


class LineItem(CreateableObject, DeleteableObject, ListableObject,
               UpdateableObject):
    pass


class Transaction(CreateableObject, DeleteableObject, ListableObject,
                  UpdateableObject):

    def send(self, **opts):
        endpoint = self.endpoint()+"/emails"
        response = self._client.request('POST', endpoint, opts)

        # build email objects
        email = Email(self._client)
        return util.build_objects(email, response['body'])

    def refund(self, **opts):
        endpoint = self.endpoint()+"/refunds"
        response = self._client.request('POST', endpoint, opts)

        return util.convert_to_object(self, response['body'])


class Subscription(CreateableObject, DeleteableObject, ListableObject,
                   UpdateableObject):

    def cancel(self):
        return self.delete()
