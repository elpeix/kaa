import sys
from wsgiref.simple_server import make_server

from . import NAME, VERSION, KaaServer
from .server import Server


class Cli:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 8086
        self.argv = sys.argv[:]
        self.server: KaaServer

    def execute(self):
        try:
            subcommand = self.argv[1]
        except IndexError:
            subcommand = "help"

        if subcommand == "version":
            msg = self.__get_version()
        elif subcommand == "help":
            msg = self.__get_help()
        elif subcommand == "serve":
            self.__serve()
            return
        else:
            msg = "Invalid command. Try help"

        sys.stdout.write(msg + "\n")

    @classmethod
    def __get_name(cls):
        return NAME

    @classmethod
    def __get_version(cls):
        return VERSION

    def __get_help(self):
        commands = [
            ("version", "Returns Kaa version"),
            ("serve", "Starts a server for development"),
        ]
        return "\n".join(["{}\t\t{}".format(*cmd) for cmd in commands])

    def __serve(self):
        self.__set_host_port()
        sys.stdout.write(
            "{} version {}\n".format(self.__get_name(), self.__get_version())
        )
        sys.stdout.write(f"Server started at {self.host}:{self.port}\n\n")
        if not hasattr(self, "server") or self.server is None:
            self.server = Server().get_server()
        make_server(
            host=self.host,
            port=int(self.port),
            app=lambda env, start_response: self.server.serve(
                env, start_response),
        ).serve_forever()

    def __set_host_port(self):
        try:
            porthost = self.argv[2].split(":")
            if len(porthost) == 1:
                self.port = porthost[0]
            elif len(porthost) == 2:
                self.host = porthost[0]
                self.port = porthost[1]
            else:
                sys.stdout.write("Invalid host:port" + "\n")
                sys.exit(1)
        except IndexError:
            pass
