from kaa.request import Request
from kaa.response import Response

class Authorization:

    def authorize(self, request:Request):
        pass

    def forbidden(self, request:Request):
        return Response().forbidden(request)