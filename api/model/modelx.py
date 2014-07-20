# coding: utf-8

import hashlib
from google.appengine.ext import ndb
from api.common.util import alpha_numeric_key


class BaseX(object):
    @classmethod
    def retrieve_one_by(cls, name, value):
        return cls.query(getattr(cls, name) == value).get()
