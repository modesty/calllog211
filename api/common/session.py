from google.appengine.api import memcache

import api.config as config

class ApiSession(object):
    @staticmethod
    def start_session(accessToken, authId):
        return memcache.set(accessToken, authId, config.SESSION_TIME_SPAN)

    @staticmethod
    def is_session_valid(accessToken, authId):
        authId_mem = memcache.get(accessToken)
        isValid = authId_mem == authId

        if authId_mem is not None and isValid:
            # reset the session timer
            memcache.set(accessToken, authId, config.SESSION_TIME_SPAN)
        else:
            isValid = False

        return isValid

    @staticmethod
    def stop_session(accessToken):
        memcache.delete(accessToken)
