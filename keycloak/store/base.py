import abc


class BaseStore():
    """
    Base class for any Token store
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_token(self, request):
        """
        Get the Oauth token.
        """
        pass

    def save_token(self, token, response):
        """
        Save the token if possible.
        """
        pass

    def remove_token(self, response):
        """
        Unset the Oauth token if possible.
        """
        pass
