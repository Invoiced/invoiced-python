from inflection import (pluralize, underscore)
from invoiced import util
import json
import re


class InvoicedObject(dict):

    def __init__(self, client, id=None, values={}):
        super(InvoicedObject, self).__init__()

        self._client = client

        # generate endpoint based on class name
        class_name = self.__class__.__name__
        self._endpoint_base = ''
        self._endpoint = '/' + pluralize(underscore(class_name)).lower()

        if id:
            self._endpoint = self._endpoint + '/' + str(id)
            self._unsaved = set()
            values.update({'id': id})
            super(InvoicedObject, self).update(values)

    def set_endpoint_base(self, base):
        self._endpoint_base = base

        return self

    def endpoint_base(self):
        return self._endpoint_base

    def endpoint(self):
        return self._endpoint_base + self._endpoint

    def retrieve(self, id, opts={}):
        if not id:
            raise ValueError("Missing ID.")

        response = self._client.request('GET',
                                        self.endpoint()+"/"+str(id),
                                        opts)

        return util.convert_to_object(self, response['body'])

    def refresh_from(self, values):
        self._unsaved = set()
        self.clear()

        for k, v in values.items():
            super(InvoicedObject, self).__setitem__(k, v)

    def update(self, update_dict):
        for k in update_dict:
            self._unsaved.add(k)

        return super(InvoicedObject, self).update(update_dict)

    def __setattr__(self, k, v):
        if k[0] == '_' or k in self.__dict__:
            return super(InvoicedObject, self).__setattr__(k, v)
        else:
            self[k] = v

    def __getattr__(self, k):
        if k[0] == '_':
            raise AttributeError(k)

        try:
            return self[k]
        except KeyError as err:
            raise AttributeError(*err.args)

    def __delattr__(self, k):
        if k[0] == '_' or k in self.__dict__:
            return super(InvoicedObject, self).__delattr__(k)
        else:
            del self[k]

    def __setitem__(self, k, v):
        if v == "":
            raise ValueError(
                "You cannot set %s to an empty string. "
                "We interpret empty strings as None in requests."
                "You may set %s.%s = None to delete the property" % (
                    k, str(self), k))

        super(InvoicedObject, self).__setitem__(k, v)

        self._unsaved.add(k)

    def __delitem__(self, k):
        super(InvoicedObject, self).__delitem__(k)

        self._unsaved.remove(k)

    def __repr__(self):
        ident_parts = [type(self).__name__]

        if self.get('id'):
            ident_parts.append('id=%s' % str(self.get('id')))

        return '<%s at %s> JSON: %s' % (
            ' '.join(ident_parts), hex(id(self)), str(self))

    def __str__(self):
        return json.dumps(self, sort_keys=True, indent=2)


class CreateableObject(InvoicedObject):

    def create(self, idempotency_key=None, **params):
        opts = {'idempotency_key': idempotency_key}
        response = self._client.request('POST', self.endpoint(), params, opts)

        return util.convert_to_object(self, response['body'])


class DeleteableObject(InvoicedObject):

    def delete(self):
        response = self._client.request('DELETE', self.endpoint())

        if response['code'] == 204:
            self.refresh_from({'id': self.id})
        elif response['code'] == 200:
            # update the local values with the response
            self.refresh_from(response['body'])

        return response['code'] == 204 or response['code'] == 200


class ListableObject(InvoicedObject):

    def list(self, **opts):
        response = self._client.request('GET', self.endpoint(), opts)

        # build objects
        objects = util.build_objects(self, response['body'])

        # store the metadata from the list operation
        metadata = List(response['headers']['link'],
                        response['headers']['x-total-count'])

        return objects, metadata


class UpdateableObject(InvoicedObject):

    def save(self, idempotency_key=None, **params):
        update = {}
        for k in self._unsaved:
            update[k] = self[k]

        update.update(params)

        # perform the update if there are any changes
        if len(update) > 0:
            opts = {'idempotency_key': idempotency_key}
            response = self._client.request('PATCH',
                                            self.endpoint(),
                                            update,
                                            opts)

            # update the local values with the response
            self.refresh_from(response['body'])

            return response['code'] == 200

        return False


class List:
    def __init__(self, link_header, total_count):
        self.links = self.parse_link_header(link_header)
        self.total_count = int(total_count)

    def parse_link_header(self, header):
        links = {}

        # Parse each part into a named link
        for part in header.split(','):
            section = part.split(';')
            url = re.search('<(.*)>', section[0]).group(1)
            name = re.search('rel="(.*)"', section[1]).group(1)
            links[name] = url

        return links
