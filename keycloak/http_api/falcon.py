from .base import BaseHTTPApi


class FalconAPI(BaseHTTPApi):
    def get_cookie(self, request, name):
        if name in request.cookies:
            return request.cookies[name]

        return None

    def set_cookie(self, response, name, value):
        response.set_cookie(name, value)

    def remove_cookie(self, response, name):
        response.unset_cookie(name)

    def get_header(self, request, name):
        return request.get_header(name)

    def original_url(self, request):
        # TODO: check whether it works for X-Forwarded-For, etc.
        return request.uri
