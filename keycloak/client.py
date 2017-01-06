import codecs
import json
import logging
from urllib.request import urlopen, Request
from urllib.parse import urlencode

from .config import Config


class Client(object):
    def __init__(self, config=None):
        if not config:
            config = Config()
        self.config = config

    def client_credentials_flow(self):
        """
        http -f --auth=user:pass https://auth.morrmusic.com/auth/realms/morrmusic_internal/protocol/openid-connect/token grant_type=client_credentials
        """
        data = {'grant_type': 'client_credentials'}
        return self.token_flow(data, auth_basic=True)

    def token_flow(self, data,
                   auth_basic=None,
                   path='/protocol/openid-connect/token', url=None):
        opts = {
            'url': url or self.config.realm_url + path,
            }

        if not isinstance(data, bytes):
            if not isinstance(data, str):
                data = urlencode(data)
            data = data.encode()

        if 'headers' not in opts:
            opts['headers'] = {}

        if 'Content-Type' not in opts['headers']:
            opts['headers']['Content-Type'] = 'application/x-www-form-urlencoded'

        if 'X-Client' not in opts['headers']:
            opts['headers']['X-Client'] = 'keycloak-python'

        if auth_basic:
            if isinstance(auth_basic, bool):
                if not self.config.client_id or not self.config.secret:
                    err = 'auth_basic: No client_id or secret given.'
                    logging.warning(err)
                    raise Exception(err)

                auth_str = self.config.client_id + ":" + self.config.secret
            else:
                # assume it's "user:pass"
                auth_str = auth_basic

            # codecs.encode does only work with bytes, is using utf8 encoded string right?
            encoded_auth_str = codecs.encode(auth_str.encode(), 'base64').decode('ascii').rstrip('\n')
            opts['headers']['Authorization'] = 'Basic ' + encoded_auth_str

        return json.loads(urlopen(Request(**opts), data).read().decode())
