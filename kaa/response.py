import json
import traceback

from definitions import DEBUG, LOG
from kaa.enums import ContentType, Status
from kaa.request import Request


class Response():

    def __init__(self, status:Status=Status.OK):
        self.responseBody = None
        self.status = status
        self.headers = dict()
        self.setContentType(ContentType.PLAIN)
    
    def body(self, responseBody:str):
        self.responseBody = responseBody
        return self
    
    def html(self, html:str):
        self.setContentType(ContentType.HTML)
        return self.body(json.dumps(html))
    
    def json(self, response:dict):
        self.setContentType(ContentType.JSON)
        return self.body(json.dumps(response))

    def getStatusCode(self):
        return self.status.value[1]

    def setContentType(self, contentType:ContentType):
        self.header('Content-Type', contentType.value)
    
    def header(self, headerName, headerValue):
        self.headers[headerName] = headerValue
        return self

    def notFound(self, request:Request):
        self.status = Status.NOT_FOUND
        return self.__setResponse(request, 'Resource not found')
    
    def forbidden(self, request:Request):
        self.status = Status.FORBIDDEN
        return self.__setResponse(request, 'Fobidden')
    
    def serverError(self, request:Request, exc_info=None):
        self.status = Status.SERVER_ERROR
        data = {}
        if exc_info:
            if DEBUG:
                data['exception'] = traceback.format_exception(*exc_info)
            else:
                LOG.error(self.status.value, exc_info=exc_info)
        return self.__setResponse(request, 'Internal server error', data)
    
    def __setResponse(self, request, message, data:dict={}):
        if request.getHeader('ACCEPT') == 'application/json':
            self.json({'status': self.status.value[0], 'message': message, **data})
        else:
            self.body(message + "\n" + str(data) if data else message)
        return self
