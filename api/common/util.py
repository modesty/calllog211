# coding: utf-8
import random
import string
from datetime import datetime
from uuid import uuid4
import re
import unicodedata
import urllib

from google.appengine.datastore.datastore_query import Cursor
from google.appengine.ext import blobstore
from google.appengine.ext import ndb
import flask

from api import config

###############################################################################
# JSON Response Helpers
###############################################################################
def jsonify_model_dbs(model_dbs, more_cursor=None):
  '''Return a response of a list of dbs as JSON service result
  '''
  result_objects = []
  for model_db in model_dbs:
    result_objects.append(model_db_to_object(model_db))

  response_object = {
      'status': 'success',
      'count': len(result_objects),
      'now': datetime.utcnow().isoformat(),
      'result': result_objects,
    }
  if more_cursor:
    response_object['more_cursor'] = more_cursor
    response_object['more_url'] = generate_more_url(more_cursor)
  response = jsonpify(response_object)
  return response


def jsonify_model_db(model_db):
  result_object = model_db_to_object(model_db)
  response = jsonpify({
      'status': 'success',
      'now': datetime.utcnow().isoformat(),
      'result': result_object,
    })
  return response


def model_db_to_object(model_db):
  model_db_object = {}
  for prop in model_db._PROPERTIES:
    if prop == 'id':
      try:
        value = json_value(getattr(model_db, 'key', None).id())
      except:
        value = None
    else:
      value = json_value(getattr(model_db, prop, None))
    if value is not None:
      model_db_object[prop] = value
  return model_db_object


def json_value(value):
  if isinstance(value, datetime):
    return value.isoformat()
  if isinstance(value, ndb.Key):
    return value.urlsafe()
  if isinstance(value, blobstore.BlobKey):
    return urllib.quote(str(value))
  if isinstance(value, ndb.GeoPt):
    return '%s,%s' % (value.lat, value.lon)
  if isinstance(value, list):
    return [json_value(v) for v in value]
  if isinstance(value, long):
    # Big numbers are sent as strings for accuracy in JavaScript
    if value > 9007199254740992 or value < -9007199254740992:
      return str(value)
  if isinstance(value, ndb.Model):
    return model_db_to_object(value)
  return value

###############################################################################
# Helpers
###############################################################################
def generate_more_url(more_cursor, base_url=None, cursor_name='cursor'):
  '''Substitutes or alters the current request URL with a new cursor parameter
  for next page of results
  '''
  if not more_cursor:
    return None
  base_url = base_url or flask.request.base_url
  args = flask.request.args.to_dict()
  args[cursor_name] = more_cursor
  return '%s?%s' % (base_url, urllib.urlencode(args))


def uuid():
  return uuid4().hex


_slugify_strip_re = re.compile(r'[^\w\s-]')
_slugify_hyphenate_re = re.compile(r'[-\s]+')


def slugify(text):
  if not isinstance(text, unicode):
    text = unicode(text)
  text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')
  text = unicode(_slugify_strip_re.sub('', text).strip().lower())
  return _slugify_hyphenate_re.sub('-', text)


def is_valid_username(username):
  return True if re.match('^[a-z0-9]+(?:[\.][a-z0-9]+)*$', username) else False


def update_query_argument(name, value=None, ignore=[], list=False):
  arguments = {}
  for key, val in flask.request.args.items():
    if key not in ignore and (list and value is not None or key != name):
      arguments[key] = val
  if value is not None:
    if list:
      values = []
      if name in arguments:
        values = arguments[name].split(',')
        del arguments[name]
      if value in values:
        values.remove(value)
      else:
        values.append(value)
      if values:
        arguments[name] = ','.join(values)
    else:
      arguments[name] = value
  query = '&'.join('%s=%s' % item for item in sorted(arguments.items()))
  return '%s%s' % (flask.request.path, '?%s' % query if query else '')


###############################################################################
# Lambdas
###############################################################################
strip_filter = lambda x: x.strip() if x else ''
email_filter = lambda x: x.lower().strip() if x else ''
sort_filter = lambda x: sorted(x) if x else []

###############################################################################
# string helpers
###############################################################################

def isStringWithLength(s, sl=None):
    retVal = isinstance(s, basestring)
    if retVal and (sl is not None):
        retVal = retVal and (len(s) == sl)
    return retVal


def isStringWithLeastLength(s, sl=1):
    retVal = isinstance(s, basestring)
    if retVal and (sl is not None):
        retVal = retVal and (len(s) >= sl)
    return retVal


###############################################################################
# convert object to dictionary
###############################################################################
def todict(obj, classkey=None):
    if isinstance(obj, dict):
        data = {}
        for (k, v) in obj.items():
            data[k] = todict(v, classkey)
        return data
    elif hasattr(obj, "_ast"):
        return todict(obj._ast())
    elif hasattr(obj, "__iter__"):
        return [todict(v, classkey) for v in obj]
    elif hasattr(obj, "__dict__"):
        data = dict([(key, todict(value, classkey))
            for key, value in obj.__dict__.iteritems()
            if not callable(value) and not key.startswith('_')])
        if classkey is not None and hasattr(obj, "__class__"):
            data[classkey] = obj.__class__.__name__
        return data
    else:
        return obj
