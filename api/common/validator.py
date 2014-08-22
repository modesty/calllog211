import random
import string
import re
import ast

from datetime import datetime
from google.appengine.ext import ndb

from werkzeug.routing import ValidationError

from api.common.util import isStringWithLength, isStringWithLeastLength
from api import config

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")
GEO_PT_REGEX = re.compile(r"^(\-?\d+(\.\d+)?),\s*(\-?\d+(\.\d+)?)$")

def ch_uuid(uuid_str):
    if isStringWithLeastLength(uuid_str, 9):
        return uuid_str
    else:
        raise ValidationError("{0} is not valid".format(uuid_str))

def ch_user_id(user_str):
    if isStringWithLeastLength(user_str, 5):
        return user_str
    else:
        raise ValidationError("{0} is not valid".format(user_str))


def ch_email(email_str):
    if EMAIL_REGEX.match(email_str):
        return email_str
    else:
        raise ValidationError("{0} is not valid".format(email_str))


def ch_geo_pt(geo_pt_str):
    if GEO_PT_REGEX.match(geo_pt_str):
        return ndb.GeoPt(geo_pt_str)
    else:
        raise ValidationError("{0} is not valid".format(geo_pt_str))

def ch_date_time(datetime_str):
    try:
        return datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
    except ValueError as e:
        raise ValidationError(e.message)

def ch_str_na(str):
    return str if isStringWithLeastLength(str, 1) else "N/A"


# value can be string, or string literal of list or tuple
def ch_literal(value):
    try:
        if isinstance(value, basestring):
            retVal = value
            if value.startswith('[') and value.endswith(']'):
                retVal = ast.literal_eval(value)
            elif value.startswith('(') and value.endswith(')'):
                retVal = ast.literal_eval(value)
            return retVal
        else:
            raise ValidationError("{} should be either string, or string literal of list or tuple".format(value))
    except Exception as e:
            raise ValidationError("'{}' should be either string, or string literal of list or tuple".format(e.message))

def ch_date_tuple(value):
    try:
        if value.startswith('(') and value.endswith(')'):
            retVal = []
            date_strs = ast.literal_eval(value)
            for one_date in date_strs:
                retVal.append(ch_date_time(one_date))
            retVal = tuple(retVal)
        else:
            retVal = ch_date_time(value)
        return retVal
    except Exception as e:
            raise ValidationError("'{}' should be either string, or string literal of tuple".format(e.message))

