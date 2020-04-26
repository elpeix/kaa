from mock import Mock
from kaa import decorators

from .decorators_test import DecoratorsTest

class DecoratorsMethodTest(DecoratorsTest):

    def testGetWrong(self):
        response = self.__testMethod(decorators.GET, 'POST')
        self.assertIsNone(response)

    def testGetValid(self):
        response = self.__testMethod(decorators.GET, 'GET')
        self.assertIsNotNone(response)

    def testPostWrong(self):
        response = self.__testMethod(decorators.POST, 'GET')
        self.assertIsNone(response)

    def testPostValid(self):
        response = self.__testMethod(decorators.POST, 'POST')
        self.assertIsNotNone(response)

    def testPutWrong(self):
        response = self.__testMethod(decorators.PUT, 'GET')
        self.assertIsNone(response)

    def testPutValid(self):
        response = self.__testMethod(decorators.PUT, 'PUT')
        self.assertIsNotNone(response)

    def testDeleteWrong(self):
        response = self.__testMethod(decorators.DELETE, 'GET')
        self.assertIsNone(response)

    def testDeleteValid(self):
        response = self.__testMethod(decorators.DELETE, 'DELETE')
        self.assertIsNotNone(response)

    def __testMethod(self, decorator, method):
        func = decorator(Mock())
        rest = self.getResource(method=method)
        return func(rest)
