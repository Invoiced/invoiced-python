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


class CatalogItem(CreateableObject, DeleteableObject, ListableObject,
                  UpdateableObject):
    pass


class Contact(CreateableObject, DeleteableObject, ListableObject,
              UpdateableObject):
    pass

class Coupon(CreateableObject, DeleteableObject, ListableObject,
              UpdateableObject):
    pass

class CreditNote(CreateableObject, DeleteableObject, ListableObject,
                 UpdateableObject):

    def send(self, idempotency_key=None, **params):
        endpoint = self.endpoint()+"/emails"
        opts = {'idempotency_key': idempotency_key}
        response = self._client.request('POST', endpoint, params, opts)

        # build email objects
        email = Email(self._client)
        return util.build_objects(email, response['body'])

    def attachments(self, **params):
        response = self._client.request('GET',
                                        self.endpoint()+"/attachments",
                                        params)

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

    def void(self):
        endpoint = self.endpoint()+'/void'
        response = self._client.request('POST', endpoint)

        # update the local values with the response
        self.refresh_from(response['body'])

        return response['code'] == 200


class Customer(CreateableObject, DeleteableObject, ListableObject,
               UpdateableObject):

    def send_statement(self, idempotency_key=None, **params):
        endpoint = self.endpoint()+"/emails"
        opts = {'idempotency_key': idempotency_key}
        response = self._client.request('POST', endpoint, params, opts)

        # build email objects
        email = Email(self._client)
        return util.build_objects(email, response['body'])

    def send_statement_sms(self, idempotency_key=None, **params):
        endpoint = self.endpoint()+"/text_messages"
        opts = {'idempotency_key': idempotency_key}
        response = self._client.request('POST', endpoint, params, opts)

        # build text message objects
        text_message = TextMessage(self._client)
        return util.build_objects(text_message, response['body'])

    def send_statement_letter(self, idempotency_key=None, **params):
        endpoint = self.endpoint()+"/letters"
        opts = {'idempotency_key': idempotency_key}
        response = self._client.request('POST', endpoint, params, opts)

        # build letter objects
        letter = Letter(self._client)
        return util.build_objects(letter, response['body'])

    def balance(self):
        endpoint = self.endpoint()+"/balance"
        response = self._client.request('GET', endpoint)

        return response['body']

    def contacts(self):
        contact = Contact(self._client)
        contact.set_endpoint_base(self.endpoint())

        return contact

    def list_notes(self):
        note = Note(self._client)
        note.set_endpoint_base(self.endpoint())

        return note

    def line_items(self):
        line = LineItem(self._client)
        line.set_endpoint_base(self.endpoint())

        return line

    def payment_sources(self):
        source = PaymentSource(self._client)
        source.set_endpoint_base(self.endpoint())

        return source

    def invoice(self, idempotency_key=None, **params):
        endpoint = self.endpoint()+"/invoices"
        opts = {'idempotency_key': idempotency_key}
        response = self._client.request('POST', endpoint, params, opts)

        # build invoice object
        invoice = Invoice(self._client)
        return util.convert_to_object(invoice, response['body'])

    def consolidate_invoices(self, **params):
        endpoint = self.endpoint()+"/consolidate_invoices"
        response = self._client.request('POST', endpoint, params)

        # build invoice object
        invoice = Invoice(self._client)
        return util.convert_to_object(invoice, response['body'])

class Email(InvoicedObject):
    pass


class Estimate(CreateableObject, DeleteableObject, ListableObject,
               UpdateableObject):

    def send(self, idempotency_key=None, **params):
        endpoint = self.endpoint()+"/emails"
        opts = {'idempotency_key': idempotency_key}
        response = self._client.request('POST', endpoint, params, opts)

        # build email objects
        email = Email(self._client)
        return util.build_objects(email, response['body'])

    def attachments(self, **params):
        response = self._client.request('GET',
                                        self.endpoint()+"/attachments",
                                        params)

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

    def invoice(self, idempotency_key=None, **params):
        endpoint = self.endpoint()+"/invoice"
        opts = {'idempotency_key': idempotency_key}
        response = self._client.request('POST', endpoint, params, opts)

        # build invoice object
        invoice = Invoice(self._client)
        return util.convert_to_object(invoice, response['body'])

    def void(self):
        endpoint = self.endpoint()+'/void'
        response = self._client.request('POST', endpoint)

        # update the local values with the response
        self.refresh_from(response['body'])

        return response['code'] == 200


class Event(ListableObject):
    pass


class File(CreateableObject, DeleteableObject):
    pass


class Invoice(CreateableObject, DeleteableObject, ListableObject,
              UpdateableObject):

    def send(self, idempotency_key=None, **params):
        endpoint = self.endpoint()+"/emails"
        opts = {'idempotency_key': idempotency_key}
        response = self._client.request('POST', endpoint, params, opts)

        # build email objects
        email = Email(self._client)
        return util.build_objects(email, response['body'])

    def send_sms(self, idempotency_key=None, **opts):
        endpoint = self.endpoint()+"/text_messages"
        opts = {'idempotency_key': idempotency_key}
        response = self._client.request('POST', endpoint, {}, opts)

        # build text message objects
        text_message = TextMessage(self._client)
        return util.build_objects(text_message, response['body'])

    def send_letter(self, idempotency_key=None, **opts):
        endpoint = self.endpoint()+"/letters"
        opts = {'idempotency_key': idempotency_key}
        response = self._client.request('POST', endpoint, {}, opts)

        # build letter objects
        letter = Letter(self._client)
        return util.build_objects(letter, response['body'])

    def pay(self, idempotency_key=None, **opts):
        endpoint = self.endpoint()+"/pay"
        opts = {'idempotency_key': idempotency_key}
        response = self._client.request('POST', endpoint, {}, opts)

        # update the local values with the response
        self.refresh_from(response['body'])

        return response['code'] == 200

    def attachments(self, **params):
        response = self._client.request('GET',
                                        self.endpoint()+"/attachments",
                                        params)

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

    def notes(self):
        note = Note(self._client)
        note.set_endpoint_base(self.endpoint())

        return note

    def payment_plan(self):
        paymentPlan = PaymentPlan(self._client)
        paymentPlan.set_endpoint_base(self.endpoint())

        return paymentPlan

    def void(self):
        endpoint = self.endpoint()+'/void'
        response = self._client.request('POST', endpoint)

        # update the local values with the response
        self.refresh_from(response['body'])

        return response['code'] == 200

class Letter(InvoicedObject):
    pass

class LineItem(CreateableObject, DeleteableObject, ListableObject,
               UpdateableObject):
    pass

class Note(CreateableObject, DeleteableObject, ListableObject,
           UpdateableObject):
    pass

class PaymentPlan(DeleteableObject):

    def __init__(self, client, id=None, values={}):
        super().__init__(client, id, values)

        self._endpoint = '/payment_plan'

    def create(self, idempotency_key=None, **params):
        opts = {'idempotency_key': idempotency_key}
        response = self._client.request('PUT', self.endpoint(), params, opts)

        return util.convert_to_object(self, response['body'])

    def retrieve(self, params={}):
        response = self._client.request('GET',
                                        self.endpoint(),
                                        params)

        return util.convert_to_object(self, response['body'])

    def cancel(self):
        return self.delete()

class PaymentSource(CreateableObject, DeleteableObject, ListableObject):
    
    def delete(self):
        if self.object == "card":
            self._endpoint = '/card/' + str(self.id)
        elif self.object == "bank_account":
            self._endpoint = '/bank_account/' + str(self.id)

        if super().delete():
            return True
        else:
            self._endpoint = "/payment_sources/" + str(self.id)
            return False


class Plan(CreateableObject, DeleteableObject, ListableObject,
           UpdateableObject):
    pass

class Subscription(CreateableObject, DeleteableObject, ListableObject,
                   UpdateableObject):

    def cancel(self):
        return self.delete()

    def preview(self, **params):
        self._endpoint = "/subscriptions/preview"
        repsonse = self._client.request('POST', self.endpoint(), params)

        return repsonse['body']

class Task(CreateableObject, DeleteableObject, ListableObject,
           UpdateableObject):
    pass

class TaxRate(CreateableObject, DeleteableObject, ListableObject,
              UpdateableObject):
    pass

class TextMessage(InvoicedObject):
    pass

class Transaction(CreateableObject, DeleteableObject, ListableObject,
                  UpdateableObject):

    def send(self, idempotency_key=None, **params):
        endpoint = self.endpoint()+"/emails"
        opts = {'idempotency_key': idempotency_key}
        response = self._client.request('POST', endpoint, params, opts)

        # build email objects
        email = Email(self._client)
        return util.build_objects(email, response['body'])

    def refund(self, idempotency_key=None, **params):
        endpoint = self.endpoint()+"/refunds"
        opts = {'idempotency_key': idempotency_key}
        response = self._client.request('POST', endpoint, params, opts)

        return util.convert_to_object(self, response['body'])

    def initiate_charge(self, idempotency_key=None, **params):
        endpoint = self._endpoint='/charges'
        opts = {'idempotency_key': idempotency_key}
        response = self._client.request('POST', endpoint, params, opts)

        return util.convert_to_object(self, response['body'])