invoiced-python
========

This repository contains the Python client library for the [Invoiced](https://invoiced.com) API.

[![CI](https://github.com/Invoiced/invoiced-python/actions/workflows/ci.yml/badge.svg)](https://github.com/Invoiced/invoiced-python/actions/workflows/ci.yml)
[![Coverage Status](https://coveralls.io/repos/Invoiced/invoiced-python/badge.svg?branch=master&service=github)](https://coveralls.io/github/Invoiced/invoiced-python?branch=master)
[![PyPI version](https://badge.fury.io/py/invoiced.svg)](https://badge.fury.io/py/invoiced)

## Installing

The Invoiced package can be installed like this:

```
pip install invoiced
```

## Requirements

- Python 3.7+
- `requests` and `inflection` libraries

## Usage

First, you must instantiate a new client

```python
import 'invoiced'

client = invoiced.Client("{API_KEY}")
```

Then, API calls can be made like this:
```python
# retrieve invoice
invoice = client.Invoice.retrieve("{INVOICE_ID}")

# mark as paid
payment = client.Payment.create(
    amount= invoice.balance,
    method= "check",
    applied_to= {
        'type': 'invoice',
        'invoice': invoice.id,
        'amount': invoice.balance
    })
```

If you want to use the sandbox API instead then you must set the second argument on the client to `True` like this:

```python
import 'invoiced'

client = invoiced.Client("{API_KEY}", True)
```

## Developing

The test suite can be run with `python setup.py test`. If you want to capture code coverage too with coverage.py then use `python -m coverage run setup.py test` and view the report with `python -m coverage report`.

Contributions must pass the [Flake8](http://flake8.pycqa.org/en/latest/) code linter.

## Deploying

The package can be uploaded to pypi with the following commands:

```
python setup.py sdist
twine upload dist/* --repository invoiced
```