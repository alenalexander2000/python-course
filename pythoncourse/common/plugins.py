"""File common plugin functions are written here."""

from hashlib import sha512
from uuid import uuid4
import json
import datetime

from logging import Handler
import requests
import traceback
from .constants import GET_IP_LOCATION
from django.http import JsonResponse
from django.db.models.fields.files import FieldFile

from .exceptions import BadRequest


class CustomJSONEncoder(json.JSONEncoder):
    """Function to encode response int JSON."""

    def default(self, o):
        """Initiation."""
        if isinstance(o, datetime.datetime):
            return o.strftime('%s')
        elif isinstance(o, FieldFile):
            try:
                return o.url
            except:
                return None
        return super(CustomJSONEncoder, self).default(o)


def _generate_key(length):
    """
    Function to generate a key.

    the following parameters is to be passed.
    :param str length: length of key
    """
    return sha512(uuid4().hex).hexdigest()[:length]


def success_response(response={}, status=200):
    """Function to create success Response."""
    response['success'] = True
    return JsonResponse(response, encoder=CustomJSONEncoder, status=status)


def error_response(exception, request=None):
    """Function to create error Response."""
    response = {}
    if isinstance(exception, ValueError):
        status = 400
        error_message = exception.message
    elif isinstance(exception, KeyError):
        status = 400
        error_message = 'Parameter missing: %s' % exception.message
    else:
        status = exception.status_code
        error_message = exception.message
        response['error_code'] = exception.status_code

    response['error_message'] = error_message
    print 'Error :  ', error_message
    response['success'] = False

    return JsonResponse(response, status=status)


class SlackLogHandler(Handler):
    """Class for slack logging."""

    def __init__(self, logging_url='', stack_trace=False):
        """Init func."""
        Handler.__init__(self)
        self.logging_url = logging_url
        self.stack_trace = stack_trace

    def emit(self, record):
        """For sending the error message to channel.."""
        print record
        message = '%s' % (record.getMessage())
        if self.stack_trace:
            if record.exc_info:
                message += '\n'.join(
                    traceback.format_exception(*record.exc_info))
                message += ('\n\n' + str(record.request))
                requests.post(
                    self.logging_url, data=json.dumps({'text': message}))


def filter_receive_data(request):
    """
    Function which identify the request method and return the req. params.

    Input Pram:
        request (obj): request object.
    Returns:
        request data
    """
    if request.method == 'POST':
        try:
            return json.loads(json.dumps(request.body))
        except:
            return request.GET
    elif request.method == 'GET':
        return request.GET
    elif request.method == 'PUT':
        return json.loads(json.dumps(request.body))
    elif request.method == 'DELETE':
        return request.GET
    else:
        pass
        # check in the url
    raise BadRequest('Invalid Request method.')


def get_location_from_ip(ip):
    """
    Function to get location from IP.

    Input Params:
        ip(str): ip address of user.
    Returns:
        location
    """
    try:
        address = ''
        location = json.loads(requests.get(GET_IP_LOCATION + ip).content)
        if location['city']:
            address = location['city'] + ', '
        if location['region_name']:
            address += location['region_name'] + ', '
        if location['country_name']:
            address += location['country_name']

        if address:
            return address
    except:
        pass
    return 'Unknown Location'
