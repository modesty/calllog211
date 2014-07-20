import sys
# from flask import request
from flask.ext.restful import Resource, reqparse, abort
from flask.ext.restful.utils import cors

from api.common.response import *
from api.common.validator import *
from api.model.model import CallLog
from api.common.util import isStringWithLength, isStringWithLeastLength

class CallLogAPI(Resource):
    # method_decorators = [cors.crossdomain(origin='*')]

    @staticmethod
    def route():
        return config.API_ROUTE_ROOT.format('calllog','')

    def parse_args(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('callReason', type=str, required=True)
        parser.add_argument('location', type=str, required=True)
        parser.add_argument('zip', type=str, required=True)
        parser.add_argument('phone', type=str, required=True)
        return parser.parse_args()

    # @cors.crossdomain(origin='*')
    def post(self):
        resObj = ResBase()

        args = self.parse_args()

        try:
            oneLog = CallLog()
            oneLog.populate(name=args.name if isStringWithLeastLength(args.name, 1) else 'N/A',
                callReason=args.callReason if isStringWithLeastLength(args.callReason, 1) else 'N/A',
                location=args.location if isStringWithLeastLength(args.location, 1) else 'N/A',
                zip=args.zip if isStringWithLength(args.zip, 5) else '00000',
                phone=args.phone if isStringWithLeastLength(args.phone, 1) else '0000000'
                )
            oneLog.put()
            resObj.result['created'] = oneLog.created.strftime('%Y-%m-%d %H:%M:%S')
            resObj.result['id'] = oneLog.key.id()
        except: # catch *all* exceptions
            e = sys.exc_info()[0]
            abort(501, Error="Exception - {0}".format(e))

        return resObj.get_json(), 200, {'Access-Control-Allow-Origin': '*'}

    def options (self):
        return {'Allow' : 'POST' }, 200, \
            { 'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods' : 'POST, OPTIONS' }