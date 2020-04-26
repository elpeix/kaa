from kaa import filters
from kaa.exceptions import NotFoundError
from kaa.request import Request
from kaa.response import Response


class OnRequest(filters.RequestFilter):
    def filter(self, request:Request):
        if request.path == '/invalid':
            raise NotFoundError('Invalid resource')

class OnResponse(filters.ResponseFilter):
    def filter(self, request:Request, response:Response):
        response.header('x-response', 'anyResponse')

class EnableCors(filters.ResponseFilter):
    def filter(self, request:Request, response:Response):
        response.header('Access-Control-Allow-Origin', 'http://localhost')
        response.header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept, Origin, Authorization')
        response.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, PATCH, OPTIONS')
