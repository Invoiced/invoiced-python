from invoiced.operations import (
    InvoicedObject,
    PaymentSourceObject,
    CreatableObject,
    DeletableObject,
    ListableObject,
    UpdatableObject,
    List)
from invoiced import util


class Attachment(InvoicedObject):
    pass


class BankAccount(PaymentSourceObject, DeletableObject):
    pass


class Card(PaymentSourceObject, DeletableObject):
    pass


class Charge(InvoicedObject):
    def create(self, idempotency_key=None, **params):
        opts = {'idempotency_key': idempotency_key}
        response = self._client.request('POST', self.endpoint(), params, opts)
        payment = Payment(self._client)

        return util.convert_to_object(payment, response['body'])


class CreditBalanceAdjustment(CreatableObject, DeletableObject,
                              ListableObject, UpdatableObject):
    pass


class Contact(CreatableObject, DeletableObject, ListableObject,
              UpdatableObject):
    pass


class Coupon(CreatableObject, DeletableObject, ListableObject,
             UpdatableObject):
    pass


class CreditNote(CreatableObject, DeletableObject, ListableObject,
                 UpdatableObject):

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


class CustomField(CreatableObject, DeletableObject,
                  ListableObject, UpdatableObject):
    pass


class Customer(CreatableObject, DeletableObject, ListableObject,
               UpdatableObject):

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


class CustomerChasingCadence(CreatableObject, DeletableObject,
                             ListableObject, UpdatableObject):
    pass


class Email(InvoicedObject):
    pass


class EmailTemplate(CreatableObject, DeletableObject,
                    ListableObject, UpdatableObject):
    pass


class Estimate(CreatableObject, DeletableObject, ListableObject,
               UpdatableObject):

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


class File(CreatableObject, DeletableObject):
    pass


class GlAccount(CreatableObject, DeletableObject,
                ListableObject, UpdatableObject):
    pass


class Inbox(ListableObject):
    pass


class Invoice(CreatableObject, DeletableObject, ListableObject,
              UpdatableObject):

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


class InvoiceChasingCadence(CreatableObject, DeletableObject,
                            ListableObject, UpdatableObject):
    pass


class Item(CreatableObject, DeletableObject, ListableObject,
           UpdatableObject):
    pass


class LateFeeSchedule(CreatableObject, DeletableObject,
                      ListableObject, UpdatableObject):
    pass


class Letter(InvoicedObject):
    pass


class LineItem(CreatableObject, DeletableObject, ListableObject,
               UpdatableObject):
    pass


class Member(CreatableObject, DeletableObject,
             ListableObject, UpdatableObject):
    pass


class MerchantAccount(CreatableObject, DeletableObject,
                      ListableObject, UpdatableObject):
    pass


class Note(CreatableObject, DeletableObject, ListableObject,
           UpdatableObject):
    pass


class Payment(CreatableObject, DeletableObject, ListableObject,
              UpdatableObject):

    def send(self, idempotency_key=None, **params):
        endpoint = self.endpoint()+"/emails"
        opts = {'idempotency_key': idempotency_key}
        response = self._client.request('POST', endpoint, params, opts)

        # build email objects
        email = Email(self._client)
        return util.build_objects(email, response['body'])


class PaymentMethod(ListableObject, UpdatableObject):
    pass


class PaymentPlan(DeletableObject):

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


class PaymentSource(CreatableObject, ListableObject):
    pass


class PdfTemplate(CreatableObject, DeletableObject,
                  ListableObject, UpdatableObject):
    pass


class Plan(CreatableObject, DeletableObject, ListableObject,
           UpdatableObject):
    pass


class Refund(InvoicedObject):

    def create(self, charge_id, idempotency_key=None, **params):
        opts = {'idempotency_key': idempotency_key}
        endpoint = self.endpoint_base()+"/charges/"+str(charge_id)+"/refunds"
        response = self._client.request('POST', endpoint, params, opts)

        return util.convert_to_object(self, response['body'])


class Report(CreatableObject):
    pass


class Role(CreatableObject, DeletableObject,
           ListableObject, UpdatableObject):
    pass


class SignUpPage(CreatableObject, DeletableObject,
                 ListableObject, UpdatableObject):
    pass


class SmsTemplate(CreatableObject, DeletableObject,
                  ListableObject, UpdatableObject):
    pass


class Subscription(CreatableObject, DeletableObject, ListableObject,
                   UpdatableObject):

    def cancel(self):
        return self.delete()

    def preview(self, **params):
        self._endpoint = "/subscriptions/preview"
        repsonse = self._client.request('POST', self.endpoint(), params)

        return repsonse['body']


class Task(CreatableObject, DeletableObject, ListableObject,
           UpdatableObject):
    pass


class TaxRate(CreatableObject, DeletableObject, ListableObject,
              UpdatableObject):
    pass


class TaxRule(CreatableObject, DeletableObject,
              ListableObject, UpdatableObject):
    pass


class TextMessage(InvoicedObject):
    pass


class Theme(CreatableObject, DeletableObject, ListableObject,
            UpdatableObject):
    pass


class Webhook(CreatableObject, DeletableObject, ListableObject,
              UpdatableObject):
    pass
