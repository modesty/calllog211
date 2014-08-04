# coding: utf-8

class BaseX(object):
    @classmethod
    def retrieve_one_by(cls, name, value):
        return cls.query(getattr(cls, name) == value).get()
