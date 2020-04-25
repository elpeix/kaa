import importlib
import sys
from .response import Response
from .request import Request
from .resources import Resources
from .enums import Status, ContentType
from .exceptions import KaaError, ResourceNotFoundError
from .filters import RequestFilter, ResponseFilter

class Rest():

    def __init__(self, env, start_response, request_filters:dict, response_filters:dict):
        self.start_response = start_response
        self.request = Request(env)
        self.request_filters = request_filters
        self.response_filters = response_filters

    def serve(self, resources:dict):
        try:
            self.__requestFilters()
            for moduleName in resources:
                for className in resources[moduleName]:
                    response:Response = self.__runResource(moduleName, className)
                    if response:
                        self.__responseFilters(response)
                        return self.__printResponse(response)
            raise ResourceNotFoundError()
        except KaaError as e:
            return self.__printResponse(e.response())
        except:
            return self.__printResponse(Response().serverError(self.request, sys.exc_info()))
    
    def __requestFilters(self):
        def func(instance:RequestFilter):
            method_ = getattr(instance, 'filter')
            method_(instance, self.request)
        self.__callFilters(self.request_filters, func)

    def __responseFilters(self, response:Response):
        def func(instance:ResponseFilter):
            method_ = getattr(instance, 'filter')
            method_(instance, self.request, response)
        self.__callFilters(self.response_filters, func)
    
    def __callFilters(self, filters, func):
        for moduleName in filters:
            for className in filters[moduleName]:
                func(self.__getClass(moduleName, className))

    def __runResource(self, moduleName, className) -> Response:
        class_ = self.__getClass(moduleName, className)
        instance:Resources = class_(self.request)
        for methodName in dir(class_):
            count = 1 + len(className) + 2
            if methodName[:2] == "__" or methodName[:count] == "_{className}__".format(className=className):
                continue
            method_ = getattr(class_, methodName)
            result = method_(instance)
            if result:
                return result
    
    def __getClass(self, moduleName, className):
        module = importlib.import_module(moduleName)
        return getattr(module, className)
    
    def __printResponse(self, response:Response):
        headers = [(k, response.headers[k]) for k in response.headers]
        headers.append(('Server', 'KAA/0.0.1'))
        self.start_response(response.getStatusCode(), headers)
        return [response.responseBody.encode("utf8")]
