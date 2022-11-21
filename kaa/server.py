import importlib
from definitions import SERVER
from kaa import KaaServer


class Server:

    def __init__(self) -> None:
        spl = SERVER.split('.')
        class_name = spl[-1]
        module_name = '.'.join(spl[:-1])
        module = importlib.import_module(module_name)
        class_ = getattr(module, class_name)
        self.server = class_()

    def get_server(self) -> KaaServer:
        return self.server

    def serve(self, env, start_response):
        return self.server.serve(env, start_response)
