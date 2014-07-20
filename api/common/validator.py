import random
import string
from datetime import datetime
from google.appengine.ext import ndb
import re

from werkzeug.routing import ValidationError

from api.common.util import isStringWithLength, isStringWithLeastLength
from api import config

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")
GEO_PT_REGEX = re.compile(r"^(\-?\d+(\.\d+)?),\s*(\-?\d+(\.\d+)?)$")


def ch_link_code(code_str):
    if isStringWithLength(code_str, 6):
        return code_str
    else:
        raise ValidationError("{0} is not valid".format(code_str))


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

def ch_access_token(token_str):
    if isStringWithLeastLength(token_str, 6):
        return token_str
    else:
        raise ValidationError("{0} is not valid".format(token_str))

def ch_oauth_provider(provider_str):
    if provider_str in config.OAUTH_PROVIDERS:
        return provider_str
    else:
        raise ValidationError("{0} is not supported".format(provider_str))


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

def ch_play_mode(mode_str):
    if mode_str in config.ENUM_PLAY_MODE:
        return mode_str
    else:
        raise ValidationError("{0} is not valid".format(mode_str))

def ch_device_type(type_str):
    if type_str in config.ENUM_DEVICE_TYPE:
        return type_str
    else:
        raise ValidationError("{0} is not valid".format(type_str))
