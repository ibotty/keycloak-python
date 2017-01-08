import logging
import json
from urllib.request import Request, urlopen
from urllib.parse import urlencode
import jose
import jose.jwt

from .grant import Grant


class GrantManager(object):
    def __init__(self, client_id, realm_url, secret=None, public=None, scope=None, not_before=None):
        self.client_id = client_id
        self.realm_url = realm_url
        self.secret = secret
        self.public = public
        self.scope = scope
        self.not_before = not_before
        self.certs = self.get_certs()

    @classmethod
    def from_config(cls, config):
        config_dict = {}

        for field in ['client_id', 'realm_url', 'secret', 'scope', 'public']:
            if hasattr(config, field):
                config_dict[field] = getattr(config, field)

        return cls(**config_dict)

    def obtain_directly(self, username, password):
        data = {
            'client_id': self.client_id,
            'username': username,
            'password': password,
            'grant_type': 'password'
        }

        return Grant.from_raw_grant(self.post_request(data))

    def obtain_from_code(self, redirect_url, code, session_id, session_host):
        data = {
            'client_session_state': session_id,
            'client_session_host': session_host,
            'code': code,
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'redirect_url': redirect_url,
        }

        return Grant.from_raw_grant(self.post_request(data))

    def ensure_freshness(self, grant):
        if not self.is_expired(grant):
            return grant

        if not grant.refresh_token:
            logging.info('Cannot refresh token: No refresh token.')
            return None

        if not self.validate_token(grant.refresh_token):
            logging.info('refresh token not valid.')
            return None

        # XXX: jwt-token
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': grant.refresh_token
        }

        return grant.update(self.post_request(data))

    def post_request(self, data, path='/protocol/openid-connect/token'):
        if not isinstance(data, str):
            data = urlencode(data)

        opts = {
            'headers': {
                'Content-Type': 'application/x-www-urlencoded',
                'X-Client': 'keycloak-python'
            },
            'url': self.realm_url + path,
            'method': 'POST',
            'data': data
        }

        if not self.public:
            auth_str = (self.client_id + ':' + self.secret).encode('base64')
            opts['headers']['Authorization'] = 'Basic ' + auth_str

        return json.loads(urlopen(Request(**opts)).read().decode('unicode'))

    def create_grant(self, raw_grant):
        if isinstance(raw_grant, str):
            grant_data = json.loads(raw_grant)
        else:
            grant_data = raw_grant

        grant = Grant(raw=raw_grant, **grant_data)
        grant = self.validate_grant(grant)

        return grant

    def validate_grant(self, grant):
        grant.access_token = self.validate_token(grant.access_token)
        grant.refresh_token = self.validate_token(grant.refresh_token)
        grant.id_token = self.validate_token(grant.id_token)

        return grant

    def validate_token(self, token):
        if self.decode_token(token):
            return token
        else:
            # logging.debug("token not valid: %s", token)

            return None

    def decode_token(self, token):
        if not token:
            return None

        try:
            decoded = jose.jwt.decode(token,
                                      key=self.certs,
                                      audience=self.client_id)
            # logging.debug('decoded token: %s', decoded)

            return decoded
        except jose.exceptions.JOSEError as e:
            # logging.info('Discarding token: %s', e)

            return None

    def get_certs(self):
        certs_url = self.realm_url + '/protocol/openid-connect/certs'
        headers = {'X-Client': 'keycloak-python'}

        raw_data = urlopen(Request(url=certs_url, headers=headers)).read()

        return json.loads(raw_data.decode())

    def is_expired(self, grant):
        if not grant.access_token:
            # logging.debug("grant's access token is not set")

            return True

        return not self.validate_token(grant.access_token)

    def login_url(self, uuid, redirect_uri):
        scopes_str = " ".join(["openid"] + self.scope)

        return ''.join([
            self.realm_url,
            '/protocol/openid-connect/auth',
            '?client_id=', self.encode_uri_component(self.client_id),
            '&state=', self.encode_uri_component(uuid),
            '&redirect_uri=', self.encode_uri_component(redirect_uri),
            '&scope=', self.encode_uri_component(scopes_str),
            '&response_type=code'])

    @staticmethod
    def encode_uri_component(s):
        pass
