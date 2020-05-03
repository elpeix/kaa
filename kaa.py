
import importlib

from kaa.cli import Cli, Server


# For WSGI application
def application(env, start_response):
    return Server().serve(env, start_response)


if __name__ == "__main__":
    cli = Cli()
    cli.execute()
