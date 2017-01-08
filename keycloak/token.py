import json
import time
from collections import namedtuple


class Token(namedtuple('Token', ['raw_token', 'client_id', 'header', 'content', 'signature', 'signed'])):
    def __new__(self, raw_token):
        self.raw_token = raw_token

        (self.header, self.signed) = raw_token.split('.', 1)
        (self.content, self.signature) = self.signed.split('.', 1)

        self.header = json.loads(self.header)
        self.content = json.loads(self.content)

    def is_expired(self):
        return self.content['exp'] * 1000 < time.time()
