from enum import Enum

class Status(Enum):
    OK = '200 Ok'
    NO_CONTENT = '202 No content'
    BAD_REQUEST = '400 Bad request'
    FORBIDDEN = '403 Forbidden'
    NOT_FOUND = '404 Not found'
    SERVER_ERROR = '500 Server error'

class ContentType(Enum):
    PLAIN = 'text/plain'
    HTML = 'text/html'
    JSON = 'application/json'