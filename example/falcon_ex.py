import falcon
import logging
from keycloak import Keycloak
from keycloak.http_api.falcon import FalconAPI


class Resource(object):
    def __init__(self, protect=False):
        self.keycloak = None
        if protect:
            self.keycloak = Keycloak(FalconAPI())

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200

        if self.keycloak:
            grant = self.keycloak.get_grant(req, resp)

            if self.keycloak.grant_has_role(grant, "resources-writer"):
                resp.body = "has role! token: %s" % self.keycloak.manager.decode_token(grant.access_token)
            else:
                try:
                    resp.body = "No role! token: %s" % self.keycloak.manager.decode_token(grant.access_token)
                except:
                    resp.body = "No valid bearer token."
        else:
            resp.body = """
            Everything a-ok.
            """

logging.basicConfig(level=logging.DEBUG)
app = falcon.API()

app.add_route('/unprotected', Resource())
app.add_route('/protected', Resource(True))
