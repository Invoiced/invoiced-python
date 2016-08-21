invoiced-python
========

This repository contains the Python client library for the [Invoiced](https://invoiced.com) API.

[![Build Status](https://travis-ci.org/Invoiced/invoiced-python.svg?branch=master)](https://travis-ci.org/Invoiced/invoiced-python)
[![Coverage Status](https://coveralls.io/repos/Invoiced/invoiced-python/badge.svg?branch=master&service=github)](https://coveralls.io/github/Invoiced/invoiced-python?branch=master)

## Installing

The Invoiced gem can be installed liked this:

```
pip install invoiced
```

## Requirements

- Python 3.3+
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
transaction = client.Transaction.create(
    invoice= invoice.id,
    amount= invoice.balance,
    method= "check")
```

If you want to use the sandbox API instead then you must set the second argument on the client to `True` like this:

```python
import 'invoiced'

client = invoiced.Client("{API_KEY}", True)
```

## Developing

The test suite can be ran with `python setup.py test`. If you want to capture code coverage too with coverage.py then use `python -m coverage run setup.py test` and view the report with `python -m coverage report`.