import unittest

from mock import MagicMock, Mock

from kaa import GET, PATH, POST, Kaa, KaaError, Resources, Response, Status


class ResourcesTest(unittest.TestCase):

    def testNotFond(self):
        self.__runKaa(
            method='GET',
            path='/notFound',
            start_response=lambda status_code, headers : self.assertEqual(status_code, Status.NOT_FOUND.value[1])
        )

    def testOk(self):
        result = self.__runKaa(
            method='GET',
            path='',
            start_response=lambda status_code, headers : self.assertEqual(status_code, Status.OK.value[1])
        )
        self.assertEqual(result, ['anyResult'.encode("utf8")])
    
    def testCausesError(self):
        self.__runKaa(
            method='POST',
            path='/error',
            start_response=lambda status_code, headers : self.assertEqual(status_code, Status.SERVER_ERROR.value[1])
        )

    def __runKaa(self, method='GET', path='', q='', start_response=None):
        env = {
            'REQUEST_METHOD' : method,
            'PATH_INFO' : path,
            'REMOTE_ADDR' : '127.0.0.1',
            'QUERY_STRING' : q
        }
        if start_response is None:
            start_response = lambda status_code, headers : print(status_code)
        kaa = Kaa(env, start_response)
        kaa.registerResources('test.resources_test', 'ResourcesFake')
        return kaa.serve()

class ResourcesFake(Resources):

    @GET
    @PATH('')
    def basicResource(self):
        return Response(Status.OK).body('anyResult')

    @POST
    @PATH('/error')
    def errorResource(self):
        raise KaaError("anyError")
