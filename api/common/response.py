from util import todict

class ResStatus(object):
    def __init__(self, code, message):
        self.code = code
        self.message = message

    def get_json(self):
        return todict(self)

class ResBase(object):
    def __init__(self):
        self.status = ResStatus(200, 'OK')
        self.result = {}

    def get_json(self):
        return todict(self)
