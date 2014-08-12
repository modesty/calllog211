import sys
# from flask import request
from flask.ext.restful import Resource, reqparse, abort

from api.common.response import *
from api.common.validator import *
from api.model.model import CallLog
from api.common.util import *

class CallLogAPI(Resource):
    @staticmethod
    def route():
        return config.API_ROUTE_ROOT.format('calllog','')

    def parse_args(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=ch_str_na, required=True)
        parser.add_argument('callReason', type=ch_str_na, required=True)
        parser.add_argument('location', type=ch_str_na, required=True)
        parser.add_argument('zip', type=ch_str_na, required=True)
        parser.add_argument('phone', type=ch_str_na, required=True)
        return parser.parse_args()

    def post(self):
        resObj = ResBase()

        args = self.parse_args()

        try:
            oneLog = CallLog(**args)
            oneLog.put()

            resObj.result['created'] = oneLog.created.strftime('%Y-%m-%d %H:%M:%S')
            resObj.result['id'] = oneLog.key.id()

        except BaseException as e:
            abort(500, Error="Exception - {0}".format(e.message))

        return resObj.get_json()