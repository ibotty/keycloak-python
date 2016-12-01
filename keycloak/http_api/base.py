import abc


class BaseHTTPApi(object):
    """
    Base class for HTTP apis
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_cookie(self, request, name):
        pass

    @abc.abstractmethod
    def set_cookie(self, response, name, value):
        pass

    @abc.abstractmethod
    def remove_cookie(self, response, name):
        pass

    @abc.abstractmethod
    def get_header(self, request, name):
        pass

    @abc.abstractmethod
    def original_url(self, request):
        pass
