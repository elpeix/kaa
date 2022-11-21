from .authorization import Authorization
from .decorators import AUTH, GET, PATH, POST, PUT, DELETE
from .enums import ContentType, Status
from .exceptions import *
from .filters import RequestFilter, ResponseFilter
from .kaa import Kaa
from .request import Request
from .resources import Resources
from .response import Response

NAME = 'KAA'
VERSION = '0.2.0'


class KaaServer:

    def __init__(self) -> None:
        self.kaa = Kaa()
        self.register_resources()
        self.register_filters()

    def register_resources(self):
        pass

    def register_filters(self):
        pass

    def serve(self, env, start_response):
        if self.kaa is None:
            raise KaaError('Kaa is not defined')
        return self.kaa.serve(env, start_response)

    def generate_openapi(self):
        pass
