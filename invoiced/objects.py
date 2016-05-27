from invoiced.operations import (
    InvoicedObject,
    CreateableObject,
    DeleteableObject,
    ListableObject,
    UpdateableObject,
    List)
from invoiced import util


class Customer(CreateableObject, DeleteableObject, ListableObject,
               UpdateableObject):

    def send_statement(self, **opts):
        response = self._client.request('POST', self.endpoint()+"/emails", opts)

        # build email objects
        email = Email(self._client)
        return util.build_objects(email, response['body'])

    def balance(self):
        response = self._client.request('GET', self.endpoint()+"/balance")

        return response['body']

    def line_items(self):
        line = LineItem(self._client)
        line.set_endpoint_base(self.endpoint())

        return line

    def invoice(self, **opts):
        response = self._client.request('POST', self.endpoint()+"/invoices", opts)

        # build invoice object
        invoice = Invoice(self._client)
        return util.convert_to_object(invoice, response['body'])


class LineItem(CreateableObject, DeleteableObject, ListableObject,
              UpdateableObject):
    pass

class Invoice(CreateableObject, DeleteableObject, ListableObject,
              UpdateableObject):

    def send(self, **opts):
        response = self._client.request('POST', self.endpoint()+"/emails", opts)

        # build email objects
        email = Email(self._client)
        return util.build_objects(email, response['body'])

    def pay(self):
        response = self._client.request('POST', self.endpoint()+"/pay")

        # update the local values with the response
        self.refresh_from(response['body'])

        return response['code'] == 200


class Transaction(CreateableObject, DeleteableObject, ListableObject,
                  UpdateableObject):

    def send(self, **opts):
        response = self._client.request('POST', self.endpoint()+"/emails", opts)

        # build email objects
        email = Email(self._client)
        return util.build_objects(email, response['body'])

    def refund(self, **opts):
        response = self._client.request('POST',
                                        self.endpoint()+"/refunds",
                                        opts)

        return util.convert_to_object(self, response['body'])


class Subscription(CreateableObject, DeleteableObject, ListableObject,
                   UpdateableObject):

    def cancel(self):
        return self.delete()


class Email(InvoicedObject):
    pass
