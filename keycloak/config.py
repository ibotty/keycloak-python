import json
import os


class Config(object):
    """
    Keycloak configuration.

    It will be read either via a keycloak.json in the cwd (or any upper
    directory), or via environment variables:
     - KEYCLOAK_REALM
     - KEYCLOAK_REALM_PUBLIC_KEY
     - KEYCLOAK_AUTH_SERVER_URL
     - KEYCLOAK_SSL_REQUIRED
     - KEYCLOAK_RESOURCE
     - KEYCLOAK_PUBLIC_CLIENT
    """
    ENV_PREFIX = "KEYCLOAK_"

    def __init__(self, scope=None, filename=None):
        """
        Load configuration from a keycloak.json file in the cwd or an upper
        directory.
        """
        filename = filename or self.find_file(os.getcwd())

        if filename:
            with open(filename, 'r') as f:
                d = json.loads(f.read())
        else:
            d = {}

        self.realm = self.get_config_key(d, "realm")
        self.realm_public_key = self.get_config_key(d, "realm-public-key")
        self.server_url = self.get_config_key(d, "server-url")
        self.auth_server_url = self.get_config_key(d, "auth-server-url", self.server_url)
        self.ssl_required = self.get_config_key(d, "ssl-required")
        self.resource = self.get_config_key(d, "resource")
        self.public = self.get_config_key(d, "public-client", False)
        self.secret = self.get_config_key(d, ["credentials", "secret"])
        self.bearer_only = self.get_config_key(d, "bearer-only", False)

        self.client_id = self.resource

        if isinstance(scope, list):
            self.scope = scope
        elif scope:
            self.scope = [scope]
        else:
            self.scope = []

        self.realm_url = self.auth_server_url + '/realms/' + self.realm
        self.realm_admin_url = self.auth_server_url + '/admin/realms/' + self.realm

    def get_config_key(self, d, key, default=None):
        """
        Get config value either from the dict or the environment.
        Key can be a string or a list; in that case the key is treated as a
        path in the dict.
        """

        if isinstance(key, str):
            key = [key]
        elif not isinstance(key, list):
            raise TypeError()

        env_name = self.ENV_PREFIX + \
            '_'.join([k.upper().replace("-", "_") for k in key])

        val = d
        try:
            for k in key:
                val = val.get(k)
        except TypeError:
            val = None
        except AttributeError:
            val = None
        val = val or os.getenv(env_name) or default

        # if not val:
        #     raise Exception("%s not set. Please use a keycloak.json or set %s." % (key, env_name))

        return val

    @staticmethod
    def find_file(path, filename="keycloak.json"):
        """
        Find a file (defaulting to keycloak.json) in path or any upper
        directories.
        """
        relfile = os.path.join(path, filename)

        if os.path.exists(relfile):
            return relfile
        else:
            # find in parent directory
            upper_dir = os.path.dirname(path)

            if path != upper_dir:
                return Config.find_file(upper_dir, filename)
            else:
                return None
