import sys
import traceback

from .enums import Status
from .response import Response


class KaaError(Exception):

    def __init__(self, msg, status:Status=Status.SERVER_ERROR, err=None):
        self.msg = msg
        self.status = status
        self.err = err
    
    def response(self):
        data = {
            "status": self.status.value[0],
            "message": self.msg
        }
        if (self.err):
            exc_info = sys.exc_info()
            data['exception'] = traceback.format_exception(*exc_info)
        return Response(self.status).json(data)
    
    def __str__(self):
        if self.err is None:
            return "{status} - {msg}".format(
                status=self.status.value[1],
                msg=self.msg
            )
        return "{status} - {msg} - {err}".format(
                status=self.status.value[1],
                msg=self.msg,
                err=repr(self.err)
            )

class NotFoundError(KaaError):
    def __init__(self, msg, err=None):
        super().__init__(msg, Status.NOT_FOUND, err)

class ResourceNotFoundError(KaaError):
    def __init__(self):
        super().__init__('Resource not found', Status.NOT_FOUND)
