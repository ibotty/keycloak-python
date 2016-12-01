"""
"""
from collections import namedtuple


class Token(namedtuple('Token', ['raw_token',
                                 'client_id',
                                 'header',
                                 'content',
                                 'signature',
                                 'signed'])):
    def __init__(self, rawtoken):
        self.raw_token = rawtoken
        (self.header, self.signed) = rawtoken.split('.', 1)
        (self.content, self.signature) = self.signed.split('.', 1)
        self.header = json.loads(self.header)
        self.content = json.loads(self.content)

    def is_expired(self):
        return this.content['exp'] * 1000 < time.time()
