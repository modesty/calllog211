# coding: utf-8
from google.appengine.ext import ndb, blobstore
from google.appengine.datastore.datastore_query import Cursor
from api import config

class BaseX(object):
    @classmethod
    def retrieve_one_by(cls, name, value):
        return cls.query(getattr(cls, name) == value).get()

    @classmethod
    def retrieve_list(cls, limit=None, order=None, cursor=None, keys_only=None, **filters):
        '''Retrieves entities from datastore, by applying cursor pagination
        and equality filters. Returns dbs or keys and more cursor value
        model_class = ndb.Model._kind_map[query.kind]
        '''
        query = cls.query()
        limit = limit or config.DEFAULT_DB_LIMIT
        orderBy = order or "-created"
        # Cursor(urlsafe=cursor)
        cursor = Cursor.from_websafe_string(cursor) if cursor else None
        model_class = cls

        for prop in filters:
            if filters.get(prop, None) is None:
                continue
            fp = filters[prop]
            mp = model_class._properties[prop]
            if isinstance(fp, list):
                nodes = [ndb.OR(mp == fi) for fi in fp]
                query = query.filter(ndb.OR(*nodes))
                # required key order: http://stackoverflow.com/questions/12449197/badargumenterror-multiquery-with-cursors-requires-key-order-in-ndb
                query = query.order(model_class._key)
            elif isinstance(fp, tuple):
                p_len = len(fp)
                if p_len == 1:
                    query = query.filter(mp != fp[0])
                elif p_len == 2:
                    query = query.filter(ndb.AND(mp >= fp[0], mp <= fp[1]))
                # unequal filters require first sort property to be the sames
                orderBy = prop + "," + orderBy
            else:
                query = query.filter(mp == fp)

        if orderBy:
            for o in orderBy.split(','):
                if o.startswith('-'):
                    query = query.order(-model_class._properties[o[1:]])
                else:
                    query = query.order(model_class._properties[o])

        model_dbs, more_cursor, more = query.fetch_page(
            limit, start_cursor=cursor, keys_only=keys_only,
        )
        # more_cursor = more_cursor.urlsafe()
        more_cursor = more_cursor.to_websafe_string() if more else None
        return list(model_dbs), more_cursor
