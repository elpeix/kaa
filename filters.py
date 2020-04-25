from kaa import filters
from kaa.request import Request
from kaa.response import Response
from kaa.exceptions import NotFoundError

class OnRequest(filters.RequestFilter):

    def filter(self, request:Request):
        if request.path == '/invalid':
            raise NotFoundError('Invalid resource')

class OnResponse(filters.ResponseFilter):
    def filter(self, request:Request, response:Response):
        response.header('x-response', 'anyResponse')