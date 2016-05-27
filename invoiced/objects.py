from invoiced.operations import (
    InvoicedObject,
    CreateableObject,
    DeleteableObject,
    ListableObject,
    UpdateableObject)
from invoiced import util


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


class LineItem(CreateableObject, DeleteableObject, ListableObject,
               UpdateableObject):
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


class Email(InvoicedObject):
    pass
