import getopt
import logging
import sys
from wsgiref.simple_server import make_server

from kaa.rest import Rest


class Kaa():

    def __init__(self):
        self.host = ''
        self.port = 8086
        self.__setArgs(sys.argv[1:])
        self.registeredClazz = dict()

    def register(self, module, clazz):
        self.registeredClazz[module] = clazz

    def __setArgs(self, argv):
        try:
            opts, args = getopt.getopt(argv,"hh:p",["host=","port="])
            logging.info("Args:", args)
        except getopt.GetoptError as e:
            logging.error("Args error", e)
            sys.exit(2)
        for opt, arg in opts:
            if opt in ("-h", "--host"):
                self.host = arg
            elif opt in ("-p", "--port"):
                self.port = arg
    
    def __serve(self, env, start_response):
        rest = Rest(env, start_response)
        return rest.serve(self.registeredClazz)
    
    def run(self):
        make_server(self.host, int(self.port), self.__serve).serve_forever()
