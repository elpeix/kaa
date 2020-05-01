import importlib
import sys

from .enums import ContentType, Status
from .exceptions import KaaError, ResourceNotFoundError
from .filters import RequestFilter, ResponseFilter
from .request import Request
from .resources import Resources
from .response import Response
import kaa


class Kaa():

    def __init__(self, env, start_response, resources:dict={}, request_filters:dict={}, response_filters:dict={}):
        self.start_response = start_response
        self.request = Request(env)
        self.resources = resources
        self.request_filters = request_filters
        self.response_filters = response_filters

    def register_resources(self, module:str, class_name:str):
        self.__register(self.resources, module, class_name)

    def register_filter_request(self, module:str, class_name):
        self.__register(self.request_filters, module, class_name)

    def register_filter_response(self, module:str, class_name):
        self.__register(self.response_filters, module, class_name)

    def __register(self, element, module, class_name):
        if module not in element:
            element[module] = []
        element[module].append(class_name)

    def serve(self):
        try:
            self.__requestFilters()
            for module_name in self.resources:
                for class_name in self.resources[module_name]:
                    response:Response = self.__run_resource(module_name, class_name)
                    if response:
                        self.__response_filters(response)
                        return self.__print_response(response)
            raise ResourceNotFoundError()
        except KaaError as e:
            return self.__print_response(e.response())
        except Exception:
            return self.__print_response(Response().server_error(self.request, sys.exc_info()))

    def __requestFilters(self):
        def func(instance:RequestFilter):
            method_ = getattr(instance, 'filter')
            method_(instance, self.request)
        self.__call_filters(self.request_filters, func)

    def __response_filters(self, response:Response):
        def func(instance:ResponseFilter):
            method_ = getattr(instance, 'filter')
            method_(instance, self.request, response)
        self.__call_filters(self.response_filters, func)

    def __call_filters(self, filters, func):
        for module_name in filters:
            for class_name in filters[module_name]:
                func(self.__get_class(module_name, class_name))

    def __run_resource(self, module_name, class_name) -> Response:
        class_ = self.__get_class(module_name, class_name)
        instance:Resources = class_(self.request)
        for method_name in dir(class_):
            count = 1 + len(class_name) + 2
            if method_name[:2] == "__" or method_name[:count] == "_{}__".format(class_name):
                continue
            method_ = getattr(class_, method_name)
            result = method_(instance)
            if result:
                return result

    def __get_class(self, module_name, class_name):
        module = importlib.import_module(module_name)
        return getattr(module, class_name)

    def __print_response(self, response:Response):
        headers = [(k, response.headers[k]) for k in response.headers]
        headers.append(('Server', '{}/{}'.format(kaa.NAME, kaa.VERSION)))
        self.start_response(response.get_status_code(), headers)
        return [response.response_body.encode("utf8")]
