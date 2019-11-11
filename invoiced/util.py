import urllib


def build_objects(_class, objects):
    return list(map(lambda obj: convert_to_object(_class, obj), objects))


def convert_to_object(_class, values):
    c = _class.__class__
    obj = c(_class._client, values['id'], values)
    obj.set_endpoint_base(_class.endpoint_base())

    return obj


def uri_encode(params):
    return '&'.join(map(lambda pair: "%s=%s" % pair, _flatten_params(params)))


def _url_encode(value):
    return urllib.parse.quote(str(value))


def _flatten_params(params, parent_key=None):
    result = []
    for key in sorted(params.keys()):
        value = params[key]
        key = _url_encode(key)
        calculated_key = parent_key+"["+key+"]" if parent_key else key
        if type(value) is dict:
            result += _flatten_params(value, calculated_key)
        elif type(value) is list:
            result += _flatten_params_array(value, calculated_key)
        else:
            result.append((calculated_key, _url_encode(value)))

    return result


def _flatten_params_array(value, calculated_key):
    result = []
    for elem in value:
        if type(elem) is dict:
            result += _flatten_params(elem, calculated_key+"[]")
        elif type(elem) is list:
            result += _flatten_params_array(elem, calculated_key)
        else:
            result.append((calculated_key+"[]", _url_encode(elem)))

    return result
