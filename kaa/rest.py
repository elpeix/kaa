import importlib
from kaa.response import Response
from kaa.request import Request
from kaa.view import View
from kaa.enums import Status, ContentType

class Rest():

    def __init__(self, env, start_response):
        self.response = start_response
        self.request = Request(env)

    def serve(self, classes):
        for module in classes:
            result:Response = self.run(module, classes[module])
            if result:
                return self.__printResult(result)
        return self.__printResult(Response().notFound(self.request))
    
    def run(self, moduleName, clazz):
        module = importlib.import_module(moduleName)
        class_ = getattr(module, clazz)
        instance:View = class_(self.request)
        for methodName in dir(class_):
            count = 1 + len(clazz) + 2
            if methodName[:2] == "__" or methodName[:count] == "_{clazz}__".format(clazz=clazz):
                continue
            method_ = getattr(class_, methodName)
            result = method_(instance)
            if result:
                return result
        return None
    
    def __printResult(self, result:Response):
        self.response(result.getStatusCode(), [
            ('Content-Type',result.getContentType()),
            ('Server', 'KAA/0.0.1')
        ])
        return [result.responseBody.encode("utf8")]