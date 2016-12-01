import json
from .base import BaseStore
from ..grant import Grant


class CookieStore(BaseStore):
    """
    Oauth2 token encoded as `Bearer` header.
    """

    def __init__(self, http_api, cookie_name='keycloak-token'):
        self.http_api = http_api
        self.cookie_name = cookie_name

    def get_token(self, request):
        cookie = self.http_api.get_cookie(request, self.cookie_name)
        if cookie:
            try:
                return json.loads(cookie)
            except json.JSONDecodeError:
                pass
        return None

    def save_grant(self, token, response):
        raw_token = token
        if isinstance(token, Grant):
            raw_token = token.raw

        self.http_api.set_cookie(response, self.cookie_name, raw_token)

    def remove_token(self, response):
        self.http_api.remove_cookie(response, self.cookie_name)
