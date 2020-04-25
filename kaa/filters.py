from .request import Request
from .response import Response

class RequestFilter():

    def filter(self, request:Request):
        pass


class ResponseFilter():

    def filter(self, request:Request, response:Response):
        pass
