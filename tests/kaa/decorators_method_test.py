from mock import Mock

from kaa import GET, POST, PUT, DELETE

from .decorators_test import TestDecorators


class TestDecoratorsMethod(TestDecorators):
    def test_get_wrong(self):
        response = self.__test_method(GET, "POST")
        self.assertIsNone(response)

    def test_get_valid(self):
        response = self.__test_method(GET, "GET")
        self.assertIsNotNone(response)

    def test_post_wrong(self):
        response = self.__test_method(POST, "GET")
        self.assertIsNone(response)

    def test_post_valid(self):
        response = self.__test_method(POST, "POST")
        self.assertIsNotNone(response)

    def test_put_wrong(self):
        response = self.__test_method(PUT, "GET")
        self.assertIsNone(response)

    def test_put_valid(self):
        response = self.__test_method(PUT, "PUT")
        self.assertIsNotNone(response)

    def test_delete_wrong(self):
        response = self.__test_method(DELETE, "GET")
        self.assertIsNone(response)

    def test_delet_valid(self):
        response = self.__test_method(DELETE, "DELETE")
        self.assertIsNotNone(response)

    def __test_method(self, decorator, method):
        func = decorator(Mock())
        rest = self.get_resource(method=method)
        return func(rest)
