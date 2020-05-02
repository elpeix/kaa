import unittest

from kaa.request import Request
from kaa.resources import Resources


class DecoratorsTest(unittest.TestCase):

    def getResource(self, method='', path='path', q=''):
        request = Request({
            'REQUEST_METHOD': method,
            'PATH_INFO': path,
            'REMOTE_ADDR': '127.0.0.1',
            'QUERY_STRING': q
        })
        return Resources(request)
