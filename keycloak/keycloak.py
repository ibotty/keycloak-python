import json
import logging

from .config import Config
from .grant_manager import GrantManager
from .store import BearerStore, CookieStore


class Keycloak(object):
    def __init__(self, http_api, config=None, stores=None):
        if not stores:
            stores = [BearerStore(http_api), CookieStore(http_api)]

        if not config:
            config = Config()

        if len(stores) == 1 and isinstance(stores[0], BearerStore):
            config.bearer_only = True

        self.config = config
        self.stores = stores
        self.manager = GrantManager.from_config(config)
        self.http_api = http_api

    def get_grant(self, request, response):
        grant_data = None

        for store in self.stores:
            raw_token = store.get_token(request)

            if not raw_token:
                # logging.debug("no token in store %s", store)

                continue

            grant_data = None

            if isinstance(raw_token, str):
                try:
                    grant_data = json.loads(raw_token)
                except json.JSONDecodeError:
                    grant_data = None
            elif isinstance(raw_token, dict):
                grant_data = raw_token

            if hasattr(grant_data, 'error'):
                # logging.info('Discarding grant because of error %s', grant_data['error'])

                grant_data = None

                continue

            break

        if grant_data:
            grant = self.manager.create_grant(grant_data)
            grant = self.manager.ensure_freshness(grant)

            if grant:
                self.store_grant(response, grant)

            return grant

    def store_grant(self, response, grant):
        for store in self.stores:
            store.save_token(response, grant)

    def can_login(self):
        return self.config.bearer_only

    def redirect_url(self, request):
        orig_url = self.http_api.original_url(request)

        if '?' in orig_url:
            query_sep = '&'
        else:
            query_sep = '?'

        return orig_url + query_sep + 'auth_callback=1'

    def force_login(self, request, response):
        # TODO
        pass

    def grant_has_role(self, grant, role):
        if not hasattr(grant, 'access_token') or not grant.access_token:
            return False

        decoded = self.manager.decode_token(grant.access_token)
        splitted = role.split(':')

        if len(splitted) == 1:
            try:
                return role in decoded['realm_access']['roles']
            except KeyError:
                # logging.info('No realm_access.roles in token')
                return False

        elif len(splitted) == 2:
            app = splitted[0]
            role = splitted[1]

            try:
                return role in decoded['resource_access'][app]
            except KeyError:
                # logging.info('No resource_access.%s in token', app)
                return False
        else:
            # logging.warning('grant_has_role: role has more than two parts separated by ":".')

            return False

    def protect(self, role, request, response):
        grant = self.get_grant(request, response)

        if grant and self.grant_has_role(grant, role):
            return

        if self.can_login():
            self.force_login(request, response)
        else:
            self.http_api.access_denied(request, response)
