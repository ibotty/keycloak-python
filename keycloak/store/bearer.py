from .base import BaseStore


class BearerStore(BaseStore):
    """
    Oauth2 token encoded as `Bearer` header.
    """

    def __init__(self, http_api):
        self.http_api = http_api

    def get_token(self, request):
        header = self.http_api.get_header(request, 'Authorization')

        if header and header.startswith('Bearer '):
            access_token = header[7:]

            return {'access_token': access_token}
