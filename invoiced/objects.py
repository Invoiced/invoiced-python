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
        response = self._client.request('POST', self._endpoint+"/emails", opts)

        # build email objects
        email = Email(self._client)
        return util.build_objects(email, response['body'])

    def balance(self):
        response = self._client.request('GET', self._endpoint+"/balance")

        return response['body']

    def subscriptions(self, **opts):
        response = self._client.request('GET',
                                        self._endpoint+"/subscriptions",
                                        opts)

        # build objects
        subscription = Subscription(self._client)
        subscriptions = util.build_objects(subscription, response['body'])

        # store the metadata from the list operation
        metadata = List(response['headers']['link'],
                        response['headers']['x-total-count'])

        return subscriptions, metadata


class Invoice(CreateableObject, DeleteableObject, ListableObject,
              UpdateableObject):

    def send(self, **opts):
        response = self._client.request('POST', self._endpoint+"/emails", opts)

        # build email objects
        email = Email(self._client)
        return util.build_objects(email, response['body'])

    def pay(self):
        response = self._client.request('POST', self._endpoint+"/pay")

        # update the local values with the response
        self.refresh_from(response['body'])

        return response['code'] == 200


class Transaction(CreateableObject, DeleteableObject, ListableObject,
                  UpdateableObject):

    def send(self, **opts):
        response = self._client.request('POST', self._endpoint+"/emails", opts)

        # build email objects
        email = Email(self._client)
        return util.build_objects(email, response['body'])

    def refund(self, **opts):
        response = self._client.request('POST',
                                        self._endpoint+"/refunds",
                                        opts)

        return util.convert_to_object(self, response['body'])


class Subscription(CreateableObject, DeleteableObject, ListableObject,
                   UpdateableObject):
    pass


class Plan(CreateableObject, DeleteableObject, ListableObject,
           UpdateableObject):
    pass


class Email(InvoicedObject):
    pass
