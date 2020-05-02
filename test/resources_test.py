import unittest
import json

from mock import MagicMock, Mock

from kaa import GET, PATH, POST, Kaa, KaaError, Resources, Response, Status


class ResourcesTest(unittest.TestCase):

    def test_not_found(self):
        self.__run_kaa(
            method='GET',
            path='/notFound',
            start_response=lambda status_code, headers: self.assertEqual(status_code, Status.NOT_FOUND.value[1])
        )

    def test_ok(self):
        result = self.__run_kaa(
            method='GET',
            path='',
            start_response=lambda status_code, headers: self.assertEqual(status_code, Status.OK.value[1])
        )
        self.assertEqual(result, ['anyResult'.encode("utf8")])

    def test_resource_no_params(self):
        self.__call_resource('', Status.BAD_REQUEST)

    def test_resource_wrong_params(self):
        q = '%20;&==&&&&=&=23'
        self.__call_resource(q, Status.BAD_REQUEST)

    def test_resource_wrong_type_params(self):
        q = 'required_param=value&int_param=string'
        self.__call_resource(q, Status.BAD_REQUEST)

    def test_resource_valid_params(self):
        q = 'basic_param=basic&required_param=value&float_param=35'
        result = self.__call_resource(q, Status.OK)[0]
        r_dict = json.loads(result, encoding='utf8')
        self.assertEqual(r_dict['id'], '1')
        self.assertEqual(r_dict['basic_param'], 'basic')
        self.assertEqual(r_dict['required_param'], 'value')
        self.assertEqual(r_dict['int_param'], 1)
        self.assertEqual(r_dict['float_param'], 35)
        self.assertEqual(type(r_dict['float_param']), type(35.0))

    def __call_resource(self, q, status:Status):
        return self.__run_kaa(
            method='GET',
            path='/resource/1',
            q=q,
            start_response=lambda status_code, headers: self.assertEqual(status_code, status.value[1])
        )

    def test_causes_error(self):
        self.__run_kaa(
            method='POST',
            path='/error',
            start_response=lambda status_code, headers: self.assertEqual(status_code, Status.SERVER_ERROR.value[1])
        )

    def __run_kaa(self, method='GET', path='', q='', start_response=None):
        env = {
            'REQUEST_METHOD': method,
            'PATH_INFO': path,
            'REMOTE_ADDR': '127.0.0.1',
            'QUERY_STRING': q
        }
        if start_response is None:
            start_response = lambda status_code, headers: print(status_code)
        kaa = Kaa(env, start_response)
        kaa.register_resources('test.resources_test', 'ResourcesFake')
        return kaa.serve()


class ResourcesFake(Resources):

    @GET
    @PATH('')
    def basic_resource(self):
        return Response(Status.OK).body('anyResult')

    @GET
    @PATH('/resource/{id}',
          query_params={
              'basic_param': {},
              'required_param': {'required': True},
              'int_param': {'type': 'int', 'default': 1},
              'float_param': {'type': 'float'}
          })
    def resource_with_params(self, id, **params):
        return Response(Status.OK).json({
            'id': id,
            **params
        })

    @POST
    @PATH('/error')
    def error_resource(self):
        raise KaaError("anyError")
