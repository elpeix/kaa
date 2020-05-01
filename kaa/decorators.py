import json
import re

from definitions import LOG
from kaa.authorization import Authorization
from kaa.enums import ContentType, Status
from kaa.exceptions import InvalidParamError
from kaa.request import Request
from kaa.response import Response


def AUTH(auth: Authorization):
    def decorator_path(func):
        def wrapper(self, **kwargs):
            if auth.authorize(self.request):
                return func(self, **kwargs)
            return auth.forbidden(self.request)
        return wrapper
    return decorator_path


def GET(func):
    def wrapper(self, **kwargs):
        if self.request.method == 'GET':
            return func(self, **kwargs)
    return wrapper


def POST(func):
    def wrapper(self, **kwargs):
        if self.request.method == 'POST':
            return func(self, **kwargs)
    return wrapper


def PUT(func):
    def wrapper(self, **kwargs):
        if self.request.method == 'PUT':
            return func(self, **kwargs)
    return wrapper


def DELETE(func):
    def wrapper(self, **kwargs):
        if self.request.method == 'DELETE':
            return func(self, **kwargs)
    return wrapper


def PATH(url, query_params:dict={}):
    def decorator_path(func):
        def wrapper(self):
            request_path = self.request.path.strip("/")
            defined_path = url.strip("/")

            q_params = QueryParams(self.request)
            if request_path == defined_path:
                params = q_params.get_params(query_params)
                return func(self, **params)

            split_request_path = request_path.split('/')
            split_defined_path = defined_path.split('/')

            if (len(split_request_path) != len(split_defined_path)):
                return

            regexp = r'^\{([a-z_][a-zA-Z0-9_]+)(:[^}]+){0,1}\}$'
            arguments = dict()
            for i in range(len(split_defined_path)):
                if split_defined_path[i] == split_request_path[i]:
                    continue
                m = re.search(regexp, split_defined_path[i])

                if m is None:
                    return

                if m.group(2):
                    pattern = re.compile(m.group(2)[1:])
                    n = re.search(pattern, split_request_path[i])
                    if (n is None):
                        return
                arguments[m.group(1)] = split_request_path[i]
                arguments.update(q_params.get_params(query_params))
            return func(self, **arguments)
        return wrapper
    return decorator_path


class QueryParams:

    params = dict()

    def __init__(self, request:Request):
        self.request = request

    def get_params(self, defined_params:dict={}):
        for k in defined_params:
            self.params[k] = self.__get_item(k, defined_params[k])
        return self.params

    def __get_item(self, defined_key, defined_value):
        q_value = self.request.get_query_param(defined_key)
        if q_value:
            if 'type' in defined_value and defined_value['type'] == 'int':
                return self.__get_int(defined_key, q_value)
            return q_value

        if 'required' in defined_value and defined_value['required']:
            raise InvalidParamError("Param {} is required".format(defined_key))

        if 'default' in defined_value:
            return defined_value['default']
    
    def __get_int(self, param, value):
        try:
            return int(value)
        except ValueError:
            raise InvalidParamError("Param {} is not a number".format(param))
