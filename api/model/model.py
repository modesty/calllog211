# coding: utf-8

from google.appengine.ext import ndb
import modelx
from api.config import *

class BaseModel(ndb.Model, modelx.BaseX):
    """
    Abstract super class for all models

    Properties:
        key, id, parent,
        created, modified, version
    """
    created = ndb.DateTimeProperty(auto_now_add=True)
    modified = ndb.DateTimeProperty(auto_now=True, indexed=False)
    version = ndb.IntegerProperty(default=CURRENT_VERSION_TIMESTAMP, indexed=False)

class CallLog(BaseModel):
    """
    Root model for CallLog
    """
    name = ndb.StringProperty(default='')
    callReason = ndb.StringProperty(default='')
    location = ndb.StringProperty(default='')
    zip = ndb.StringProperty(default='')
    phone = ndb.StringProperty(default='')
