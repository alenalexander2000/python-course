"""Common aiding functions for all apps."""

import datetime
import re
from time import mktime
import pytz
import string

from django.utils import timezone
from django.utils.timezone import localtime

from PIL import Image
import ast
import json
import requests
import tinyurl
from six import string_types

from django.core.validators import validate_email
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from .constants import DEFAULT_LIMIT
from .constants import DEFAULT_OFFSET
from .constants import INT
from .constants import FLOAT
from .constants import STR
from .constants import EMAIL
from .constants import BOOL
from .constants import DATE
from .constants import PASS
from .constants import IMAGE
from .constants import FILE
from .constants import LIST
from .constants import GET_LIST
from .constants import DICT
from .constants import INTBOOL

from .exceptions import BadRequest


def fetch_request_params(request_dict):
    """
    Function to collect the parameters in request.

    Input params:
        request_dict (obj): object which contains,
            mandatory_params (list): parameter list, which should be
                in the request.
            optional_params (list): parameters, which is optional
            media_params(list): media data.
            received_data (dict): json dictionary which contains the parameters
                in the parameter list.
    Return:
        param_dict (obj): object which has the collected parameters.
    """
    param_dict = {}
    if 'mandatory_params' in request_dict.keys():
        fetch_mandatory_params(request_dict, param_dict)

    if 'optional_params' in request_dict.keys():
        fetch_optional_params(request_dict, param_dict)

    if 'media_params' in request_dict.keys():
        fetch_media_params(request_dict, param_dict)
    return param_dict


def fetch_mandatory_params(request_dict, param_dict):
    """Function to fetch the mandatory parameters in request."""
    for item in request_dict['mandatory_params']:
        parameter = item[0]
        value = request_dict['received_data'].get(parameter)
        if not value:
            raise KeyError('%s is missing in request params' % (parameter))
        else:
            value_dict = {}
            value_dict['value'] = value
            value_dict['parameter'] = parameter
            value_dict['type'] = item[1]
            value = check_parameter_value(value_dict)

        param_dict[parameter] = value
    return param_dict


def fetch_optional_params(request_dict, param_dict):
    """Function to fetch the optional parameters in request."""
    for item in request_dict['optional_params']:
        parameter = item[0]
        value = request_dict['received_data'].get(parameter)
        if value:
            value_dict = {}
            value_dict['value'] = value
            value_dict['parameter'] = parameter
            value_dict['type'] = item[1]
            value = check_parameter_value(value_dict)

            param_dict[parameter] = value
    return param_dict


def fetch_media_params(request_dict, param_dict):
    """Function to fetch the media parameters in request."""
    for item in request_dict['media_params']:
        parameter = item[0]
        value = request_dict['files'].get(parameter)
        if not value:
            raise KeyError('%s is missing in request params' % (parameter))
        else:
            value_dict = {}
            value_dict['value'] = value
            value_dict['parameter'] = parameter
            value_dict['type'] = item[1]
            value = check_parameter_value(value_dict)

        param_dict[parameter] = value
    return param_dict


def check_parameter_value(value_dict):
    """
    Function to check the parameter vales and type.

    Input Params:
        value_dict (obj): collection obj with following data,
            value: value collected
            parameter: parameter name.
            type: value type
    """
    if value_dict['type'] == INT:
        return(check_int_value(value_dict))
    if value_dict['type'] == FLOAT:
        return(check_float_value(value_dict))
    elif value_dict['type'] == STR:
        return(check_str_value(value_dict))
    elif value_dict['type'] == EMAIL:
        return(check_email_value(value_dict))
    elif value_dict['type'] == BOOL:
        return(check_bool_value(value_dict))
    elif value_dict['type'] == DATE:
        return(check_date_value(value_dict))
    elif value_dict['type'] == PASS:
        return(check_password(value_dict))
    elif value_dict['type'] == IMAGE:
        return(check_image_value(value_dict))
    elif value_dict['type'] == FILE:
        return(value_dict['value'])
    elif value_dict['type'] == LIST:
        return(check_list_value(value_dict))
    elif value_dict['type'] == GET_LIST:
        return(check_get_list_value(value_dict))
    elif value_dict['type'] == DICT:
        return(check_get_dictionary_value(value_dict))
    elif value_dict['type'] == INTBOOL:
        return(check_int_bool_value(value_dict))
    else:
        raise ValueError('Invalid parameter type')


def check_int_bool_value(value_dict):
    """
    Function to check the int bool value.

    Int value is representing the bool values false or
    true with 1 and 2 respectively.
    """
    try:
        value = int(value_dict['value'])
        if value == 1:
            return False
        elif value == 2:
            return True
        else:
            raise ValueError(
                '%s must be either 1 or 2' % (value_dict['parameter']))
    except:
        raise ValueError('%s must be int' % (value_dict['parameter']))


def check_int_value(value_dict):
    """Function to check the int value, and return the value."""
    try:
        return int(value_dict['value'])
    except:
        raise ValueError('%s must be int' % (value_dict['parameter']))


def check_float_value(value_dict):
    """Function to check the float value, and return the value."""
    try:
            return float(value_dict['value'])
    except:
        raise ValueError('%s must be float' % (value_dict['parameter']))


def check_str_value(value_dict):
    """Function to check the str value, and return the value."""
    if isinstance(value_dict['value'], string_types):
        return (value_dict['value'])
    else:
        raise ValueError('%s must be str' % (value_dict['parameter']))


def check_email_value(value_dict):
    """Function to check the email value, and return the value."""
    try:
        validate_email(value_dict['value'])
    except:
        raise ValueError(
            '%s is not in valid format.' % (value_dict['parameter']))
    return value_dict['value']


def check_bool_value(value_dict):
    """Function to check the bool value, and return the value."""
    try:
        value = value_dict['value'].lower()
    except:
        value = str(value_dict['value']).lower()
    if value == 'true':
        return True
    elif value == 'false':
        return False
    raise ValueError(
        '%s must be true or false value.' % (value_dict['parameter']))


def check_date_value(value_dict):
    """Function to check the date value, and return the value."""
    try:
        return convert_to_datetime_from_unix(
            float(value_dict['value']))
    except:
        raise ValueError(
            '%s must be Unix time stamp value' % (value_dict['parameter']))


def check_password(value_dict):
    """Function to check the password validity."""
    password = value_dict['value']
    validity = check_password_validity(password)
    validity['valid']
    if not validity['valid']:
        raise ValueError(validity['message'])
    return password


def check_image_value(value_dict):
    """Function to check the image value, and return the value."""
    try:
        image = Image.open(value_dict['value'])
        image.verify()
        return (value_dict['value'])
    except:
        raise ValueError(
            '%s should be in proper picture format.' % (
                value_dict['parameter']))


def check_list_value(value_dict):
    """Function to check the list value, and return the value."""
    value = value_dict['value']
    if type(value) == unicode or type(value) == str:
        try:
            value = eval(value)
            if type(value) != list:
                value = list(value)
            return value
        except:
            raise ValueError(
                '%s must be list.' % (value_dict['parameter']))
    try:
        return list(value_dict['value'])
    except:
        raise ValueError(
            '%s must be list.' % (value_dict['parameter']))


def check_get_list_value(value_dict):
    """Function to check the list value from get method."""
    try:
        value = ast.literal_eval(value_dict['value'])
        return list(value)
    except:
        raise ValueError(
            '%s must be list.' % (value_dict['parameter']))


def check_get_dictionary_value(value_dict):
    """Function to check the dictionary value from get method."""
    try:
        return (value_dict['value'])
    except:
        raise ValueError(
            '%s must be dictionary.' % (value_dict['parameter']))


def check_password_validity(password):
    """
    Function to check password validity.

    Input Params:
        password(str): password
    Returns:
        (dict): with
            valid(bool): true of false status of validity.
            message(str): message
    """
    data = {}
    try:
        password_validation.validate_password(password)
        data['valid'] = True
        data['message'] = 'Valid Password.'
    except ValidationError as e:
        data['valid'] = False
        data['message'] = '; '.join(e.messages)
    return data


def get_receive_data(request):
    """
    Function which identify the request method and return the req. params.

    Input Pram:
        request (obj): request object.
    Returns:
        request data
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            if not data:
                data = request.GET
            return data
        except:
            return request.GET
    elif request.method == 'GET':
        return request.GET
    elif request.method == 'PUT':
        return json.loads(request.body)
    elif request.method == 'DELETE':
        return request.GET
    else:
        pass
        # check in the url
    raise BadRequest('Invalid request method.')


def get_file_url(file):
    """
    Function to check if file is available and return URL.

    Input Para:
        file (img): file object.
    Returns:
        (url): URL of the file.
    """
    if file:
        return file.url
    return None


def set_limit_and_offset(param_dict):
    """Function to set limit and offset."""
    if not('limit' in param_dict.keys()):
            param_dict['limit'] = DEFAULT_LIMIT
    if not('offset' in param_dict.keys()):
        param_dict['offset'] = DEFAULT_OFFSET
    return param_dict


def update_object_list_with_limit(param_dict):
    """Function which will apply the limit and offset."""
    set_limit_and_offset(param_dict)
    try:
        return param_dict['objects'][
            param_dict['offset']: param_dict['offset'] + param_dict['limit']]
    except:
        raise BadRequest('Invalid Limit and offset.')


def get_paginator_meta_data(param_dict):
    """
    Function to prepare the meta data.

    Function accept the limit and offset value and make the
    meta data for pagination from it.
    Input Para:
        param_dict(dict): Collection object with following parameters,
            limit (int) : limit
            offset(int) : offset
            objects(q_list) : total objects fetched
        Returns:
            (dict): with following details,
                next_offset(int) : next offset to fetch next set of values
                limit(int) : limit
                count(int) : total no items to fetch
                previous_offset(int) : previous offset to fetch previous items.
    """
    set_limit_and_offset(param_dict)
    count = param_dict['objects'].count()
    start = param_dict['offset']
    if param_dict['limit'] > 0:
        end = start + param_dict['limit']
        if end < count:
            next_offset = end
        else:
            next_offset = None
    else:
        end = count
        next_offset = None
    if start - param_dict['limit'] >= 0:
        previous_offset = start - param_dict['limit']
    else:
        previous_offset = None
    meta = {
        'next_offset': next_offset, 'limit': param_dict['limit'],
        'count': count, 'previous_offset': previous_offset
    }
    return meta


def get_date_time(date):
    """Function to format date time."""
    try:
        date = localtime(date)
    except:
        pass
    return date.strftime('%d %B %Y, %H:%M %p')


def get_date(date):
    """Function to format date."""
    try:
        date = localtime(date)
    except:
        pass
    return date.strftime('%d %B %Y')


def get_day_month(date):
    """Function to format date."""
    # try:
    #     date = localtime(date)
    # except:
    #     pass
    return date.strftime('%d %B')


def get_due_date(date):
    """
    Function to get due date description.

    Input Params:
        date(datetime): date
    Returns:
        message(str): descriptions
    """
    try:
        if isinstance(date, datetime.date):
            difference = (date - timezone.now().date()).days
        else:
            difference = (date - timezone.now()).days
        if difference > 0:
            message = 'due date in '
        elif difference < 0:
            message = 'over due for '
        else:
            message = 'due date today'
        difference = abs(difference)

        if 1 < difference < 7:
            message += '%s days' % str(difference)
        if difference == 1:
            message += 'a day'

        elif difference > 7:
            weeks = difference / 7
            if 1 < weeks < 6:
                message += '%s weeks' % str(weeks)
            elif weeks == 1:
                message += 'a week'
            elif weeks > 5:
                months = weeks / 4
                if months > 1:
                    message += '%s months' % str(months)
                elif months == 1:
                    message += 'a month'

        return message
    except:
        return 'soon'


def calculate_percentage(part, whole):
    """Function which calculate the percentage of 2 numbers."""
    try:
        return round((100 * float(part) / float(whole)), 2)
    except:
        return 0


def check_for_input_params_of_function(input_dict):
    """Function to check the input values."""
    for key in input_dict['inputs']:
        if not (key in input_dict.keys()):
            raise ValueError(
                '%s is missing in input params.' % (key))
    return True


def check_special_characters_in_string(word, alloweds):
    """Function to check the special chars in string."""
    for allowed in alloweds:
        invalid_chars = set(string.punctuation.replace(allowed, ""))
    if any(letter in invalid_chars for letter in word):
        raise ValueError('Special characters are not allowed')
    return True


def convert_to_str(value):
    """Function to convert value to str."""
    if isinstance(value, string_types):
        return value
    else:
        try:
            return str(value)
        except:
            raise BadRequest('String conversion failed.')


def conver_to_int(value):
    """Function to convert value to int."""
    try:
        return int(value)
    except:
        try:
            value = re.sub('[^0-9]', '', value)
            return int(value)
        except:
            return 0


def conver_to_float(value):
    """Function to convert value to int."""
    try:
        return float(value)
    except:
        try:
            value = re.sub('[^0-9], .', '', value)
            return float(value)
        except:
            return 0.0


def conver_to_dictionary(value):
    """Function to convert value to int."""
    try:
        return eval(value)
    except:
        return {}


def convert_to_datetime_from_unix(unix_time):
    """Function to convert Unix timestamps to date time."""
    if not isinstance(unix_time, (int, long, float)):
        raise ValueError('Unix timestamps must be float')

    date = datetime.datetime.utcfromtimestamp(unix_time)
    date = date.replace(tzinfo=pytz.UTC)
    return date


def convert_to_unix_from_datetime(date):
    """Function to convert Unix timestamps to date time."""
    try:
        unix = mktime(date.timetuple())
    except:
        unix = 0.0

    return unix


def convert_sec_to_min(seconds):
    """Function to convert seconds to minute."""
    if seconds:
        seconds = int(seconds)
    else:
        seconds = 0
    return '%02d:%02d' % (divmod(seconds, 60))


def convert_list_to_words(word_list):
    """Function to convert list to word."""
    length = len(word_list)
    words = ''
    position = 1
    for word in word_list:
        try:
            word = str(word)
        except:
            continue
        words += word
        if position == length - 1:
            words += ' and '
        else:
            if length > 1 and position != length:
                words += ', '
        position += 1
    return words


def remove_keys_from_dictionary(dictionary, keys):
    """
    Function to remove keys from dictionary.

    Input Params:
        dictionary(dict): dictionary
        keys(list)
    Returns:
        dictionary(dictionary): updated dictionary.
    """
    for key in keys:
        dictionary.pop(key, None)
    return dictionary


def short_url(url):
    """
    Function to shorten URL using tinyurl

    Input params:
        url(str): the url to be shortened.
    returns:
        short_url(str): the short url
    """
    post_url = 'https://firebasedynamiclinks.googleapis.com/v1/shortLinks?key=AIzaSyCnfYI2R82nQcC4F6mLbnEIBP2kaiJM2Co'
    payload = {
        "dynamicLinkInfo": {
            "dynamicLinkDomain": "uebt.page.link",
            "link": url,
            }
    }
    headers = {'content-type': 'application/json'}
    try:
        response = requests.post(post_url, data=json.dumps(payload), headers=headers)
    except:
        BadRequest('generating shortened url failed, invalid url format')
    json_dict = json.loads(response.text)
    return json_dict['shortLink']
