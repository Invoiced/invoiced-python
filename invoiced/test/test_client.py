import unittest
import invoiced
import responses
import json
from requests.exceptions import HTTPError


class TestClient(unittest.TestCase):

    def test_new_client(self):
        client = invoiced.Client('api_key')

        self.assertEqual('api_key', client.api_key)
        self.assertEqual('https://api.invoiced.com', client.api_url)
        self.assertIsInstance(client.Customer, invoiced.Customer)
        self.assertIsInstance(client.Invoice, invoiced.Invoice)
        self.assertIsInstance(client.Transaction, invoiced.Transaction)
        self.assertIsInstance(client.Subscription, invoiced.Subscription)

    def test_new_client_sandbox(self):
        client = invoiced.Client('api_key', True)

        self.assertEqual('api_key', client.api_key)
        self.assertEqual('https://api.sandbox.invoiced.com', client.api_url)
        self.assertIsInstance(client.Customer, invoiced.Customer)
        self.assertIsInstance(client.Invoice, invoiced.Invoice)
        self.assertIsInstance(client.Transaction, invoiced.Transaction)
        self.assertIsInstance(client.Subscription, invoiced.Subscription)

    @responses.activate
    def test_get_request(self):
        def request_callback(request):
            # verify headers
            self.assertEqual(request.headers['authorization'], "Basic dGVzdDo=")  # noqa
            self.assertEqual(request.headers['content-type'], "application/json")  # noqa
            self.assertEqual(request.headers['user-agent'], "Invoiced Python/" + invoiced.VERSION)  # noqa

            headers = {'Header': 'test', 'Content-Type': 'application/json'}
            body = {'test': True}
            return (200, headers, json.dumps(body))

        responses.add_callback(responses.GET,
                               'https://api.invoiced.com/invoices?filter[levels]=work&test=property',  # noqa
                               match_querystring=True,
                               callback=request_callback)

        client = invoiced.Client('test')

        params = {
            'test': 'property',
            'filter': {
                'levels': 'work'
            }
        }
        response = client.request('GET', '/invoices', params)

        expectedResponse = {
            'code': 200,
            'headers': {
                'Header': 'test',
                'Content-Type': 'application/json'
            },
            'body': {
                'test': True
            }
        }
        self.assertEqual(response, expectedResponse)

    @responses.activate
    def test_post_request(self):
        responses.add(responses.POST,
                      'https://api.invoiced.com/invoices',
                      status=204,
                      adding_headers={'Header': 'test'})

        client = invoiced.Client('test')

        params = {
            "test": "property"
        }
        response = client.request("POST", "/invoices", params)

        expectedResponse = {
            'code': 204,
            'headers': {
                'Header': 'test',
                'Content-Type': 'text/plain'
            },
            'body': None
        }
        self.assertEqual(response, expectedResponse)

    @responses.activate
    def test_post_idempotent_request(self):
        responses.add(responses.POST,
                      'https://api.invoiced.com/invoices',
                      status=204,
                      adding_headers={'Header': 'test'})

        client = invoiced.Client('test')

        params = {
            "test": "property"
        }
        opts = {
            "idempotency_key": "a random value"
        }
        response = client.request("POST", "/invoices", params, opts)

        expectedResponse = {
            'code': 204,
            'headers': {
                'Header': 'test',
                'Content-Type': 'text/plain'
            },
            'body': None
        }
        self.assertEqual(response, expectedResponse)

    @responses.activate
    def test_request_exception(self):
        responses.add(responses.GET,
                      'https://api.invoiced.com/invoices',
                      body=HTTPError('Something went wrong'))

        client = invoiced.Client('test')

        with self.assertRaises(invoiced.errors.ApiConnectionError):
            client.request("GET", "/invoices")

    @responses.activate
    def test_invalid_request_error(self):
        responses.add(responses.POST,
                      'https://api.invoiced.com/invoices',
                      json={'message': 'error'},
                      status=400)

        client = invoiced.Client('test')

        with self.assertRaises(invoiced.errors.InvalidRequestError):
            client.request("POST", "/invoices")

    @responses.activate
    def test_rate_limit_error(self):
        responses.add(responses.POST,
                      'https://api.invoiced.com/invoices',
                      json={'message': 'error'},
                      status=429)

        client = invoiced.Client('test')

        with self.assertRaises(invoiced.errors.RateLimitError):
            client.request("POST", "/invoices")

    @responses.activate
    def test_authentication_error(self):
        responses.add(responses.POST,
                      'https://api.invoiced.com/invoices',
                      json={'message': 'error'},
                      status=401)

        client = invoiced.Client('test')

        with self.assertRaises(invoiced.errors.AuthenticationError):
            client.request("POST", "/invoices")

    @responses.activate
    def test_api_error(self):
        responses.add(responses.POST,
                      'https://api.invoiced.com/invoices',
                      json={'message': 'error'},
                      status=500)

        client = invoiced.Client('test')

        with self.assertRaises(invoiced.errors.ApiError):
            client.request("POST", "/invoices")

    @responses.activate
    def test_api_error_invalid_json(self):
        responses.add(responses.POST,
                      'https://api.invoiced.com/invoices',
                      body='not valid json',
                      content_type='application/json',
                      status=400)

        client = invoiced.Client('test')

        with self.assertRaises(invoiced.errors.ApiError):
            client.request("POST", "/invoices")


if __name__ == '__main__':
    unittest.main()
