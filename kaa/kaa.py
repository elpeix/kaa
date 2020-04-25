import getopt
import logging
import sys
from wsgiref.simple_server import make_server

from definitions import DEBUG, LOG
from kaa.rest import Rest


class Kaa():

    def __init__(self):
        self.host = ''
        self.port = 8086
        self.__setArgs(sys.argv[1:])
        self.resources = dict()
        self.request_filters = dict()
        self.response_filters = dict()

    def registerResources(self, module:str, className:str):
        self.__register(self.resources, module, className)
    
    def registerFilterRequest(self, module:str, className):
        self.__register(self.request_filters, module, className)

    def registerFilterResponse(self, module:str, className):
        self.__register(self.response_filters, module, className)

    def __register(self, element, module, className):
        if module not in element:
            element[module] = []
        element[module].append(className)

    def __setArgs(self, argv):
        try:
            opts, args = getopt.getopt(argv,"hh:p",["host=","port="])
            if DEBUG:
                LOG.info("Args:", args=args)
        except getopt.GetoptError as e:
            LOG.error("Error", exc_info=e)
            sys.exit(2)
        for opt, arg in opts:
            if opt in ("-h", "--host"):
                self.host = arg
            elif opt in ("-p", "--port"):
                self.port = arg
    
    def __serve(self, env, start_response):
        rest = Rest(env, start_response, self.request_filters, self.response_filters)
        return rest.serve(self.resources)
    
    def run(self):
        make_server(self.host, int(self.port), self.__serve).serve_forever()
