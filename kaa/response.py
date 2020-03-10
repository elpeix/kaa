from kaa.enums import Status, ContentType
from kaa.request import Request
import json

class Response():

    def __init__(self, status:Status=Status.OK):
        self.responseBody = None
        self.status = status
        self.contentType = ContentType.PLAIN
    
    def body(self, responseBody:str):
        self.responseBody = responseBody
        return self
    
    def html(self, html:str):
        self.contentType = ContentType.HTML
        return self.body(json.dumps(html))
    
    def json(self, response:dict):
        self.contentType = ContentType.JSON
        return self.body(json.dumps(response))

    def getStatusCode(self):
        return self.status.value

    def setContentType(self, contentType:ContentType):
        self.contentType = contentType

    def getContentType(self):
        return self.contentType.value

    def notFound(self, request:Request):
        self.status = Status.NOT_FOUND
        return self.__setResponse(request, 404, 'Resource not found')
    
    def forbidden(self, request:Request):
        self.status = Status.FORBIDDEN
        return self.__setResponse(request, 403, 'Fobidden')
    
    def __setResponse(self, request, statusCode, message):
        if request.getHeader('ACCEPT') == 'application/json':
            self.contentType = ContentType.JSON
            self.json({'status': statusCode, 'message': message})
        else:
            self.contentType = ContentType.PLAIN
            self.body(message)
        
        return self