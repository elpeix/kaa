from kaa.cli import Cli, Server

# For WSGI application
def application(env, start_response):
    return Server().serve(env, start_response)
