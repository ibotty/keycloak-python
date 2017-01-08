"""
The Grant holds the access token, refresh token and associated data.
"""
import logging


class Grant(object):
    def __init__(self,
                 access_token=None,
                 refresh_token=None,
                 id_token=None,
                 raw=None):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.id_token = id_token
        self.raw = raw

        logging.error('grant__init__: %s', self.__dict__)

    @classmethod
    def from_raw_grant(cls, grant):
        return cls().update(grant)

    def update(self, grant):
        def wrap(key):
            try:
                if isinstance(grant, dict):
                    val = grant[key]
                else:
                    val = getattr(grant, key)
                if val:
                    setattr(self, key, val)
                else:
                    logging.error('not setting attribute to null: %s', key)
            except KeyError:
                pass
            except AttributeError:
                pass

        wrap('access_token')
        wrap('refresh_token')
        wrap('id_token')
        wrap('expires_in')

        self.raw = grant

        return grant
