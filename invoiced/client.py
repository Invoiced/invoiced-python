from invoiced.objects import (
    CatalogItem,
    CreditNote,
    Customer,
    Estimate,
    Event,
    File,
    Invoice,
    Plan,
    Transaction,
    Subscription)
from invoiced import errors, util, version
import json
import requests
from requests.auth import HTTPBasicAuth


class Client(object):

    ApiBase = 'https://api.invoiced.com'
    ApiBaseSandbox = 'https://api.sandbox.invoiced.com'

    def __init__(self, api_key, sandbox=False):
        self.api_key = api_key
        self.sandbox = sandbox
        self.api_url = self.ApiBaseSandbox if sandbox else self.ApiBase

        # Object endpoints
        self.CatalogItem = CatalogItem(self)
        self.CreditNote = CreditNote(self)
        self.Customer = Customer(self)
        self.Estimate = Estimate(self)
        self.Event = Event(self)
        self.File = File(self)
        self.Invoice = Invoice(self)
        self.Plan = Plan(self)
        self.Subscription = Subscription(self)
        self.Transaction = Transaction(self)

    def request(self, method, endpoint, params={}, opts={}):
        url = self.api_url + endpoint

        # These methods don't have a request body
        if method in ('GET', 'HEAD', 'DELETE'):
            payload = None
            # Make params into GET parameters
            if len(params) > 0:
                url = url + "?" + util.uri_encode(params)
        # Otherwise, encode request body to JSON
        else:
            payload = json.dumps(params, separators=(',', ':'))

        try:
            resp = requests.request(method, url,
                                    headers=self.build_headers(opts),
                                    data=payload,
                                    auth=HTTPBasicAuth(self.api_key, ''))

            if (resp.status_code >= 400):
                self.handle_api_error(resp)
        except requests.exceptions.RequestException as e:
            self.handle_network_error(e)

        return self.parse(resp)

    def build_headers(self, opts):
        headers = {
            'content-type': "application/json",
            'user-agent': "Invoiced Python/"+version.VERSION
        }

        # idempotency keys
        if "idempotency_key" in opts and opts["idempotency_key"]:
            headers["idempotency-key"] = opts["idempotency_key"]

        return headers

    def parse(self, response):
        if response.status_code == 204:
            parsed_response = None
        else:
            parsed_response = json.loads(response.text)

        return {
            'code': response.status_code,
            'headers': response.headers,
            'body': parsed_response
        }

    def handle_api_error(self, response):
        try:
            error = json.loads(response.text)
        except:
            raise self.general_api_error(response.status_code, response.text)

        if response.status_code in (400, 403, 404):
            raise self.invalid_request_error(error, response)
        elif response.status_code == 401:
            raise self.authentication_error(error, response)
        elif response.status_code == 429:
            raise self.rate_limit_error(error, response)
        else:
            raise self.api_error(error, response)

    def handle_network_error(self, error):
        raise errors.ApiConnectionError("There was an error connecting to "
                                        "Invoiced. Please check your internet "
                                        "connection or status.invoiced.com "
                                        "for service outages. The reason was: "
                                        + str(error))

    def authentication_error(self, error, response):
        return errors.AuthenticationError(error["message"],
                                          response.status_code,
                                          error)

    def invalid_request_error(self, error, response):
        return errors.InvalidRequestError(error["message"],
                                          response.status_code,
                                          error)

    def rate_limit_error(self, error, response):
        return errors.RateLimitError(error["message"],
                                     response.status_code,
                                     error)

    def api_error(self, error, response):
        return errors.ApiError(error["message"], response.status_code, error)

    def general_api_error(self, code, body):
        return errors.ApiError("API Error " + str(code) + " - " +
                               str(body), code)
