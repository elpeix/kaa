# Kaa
A very simple python server framework for REST applications.

## Starting

### Requirements

- pyYaml for OpenApi output

### Install

```bash
pip install kaa-rest-server
```

### Main files

#### Definitions

Requires file definitions.py at the top of the project:

```python
import logging


NAME = 'Simple kaa Server'  # Your project name
VERSION = 'v1.0'  # Version 
SERVER = 'server.Server'  # Module and main class

LOG = logging.getLogger()
DEBUG = True
ENABLE_CORS = False

```

#### Application file

Requires a simple file to start server (app.py)

```python
import importlib

from kaa.cli import Cli, Server


# For WSGI application
def application(env, start_response):
    return Server().serve(env, start_response)


# For development
if __name__ == "__main__":
    cli = Cli()
    cli.execute()

```

#### Main classes

(file server.py)

This class initializes Kaa for each http request

```python
from kaa import Kaa, KaaServer

class Server(KaaServer):

    def register_resources(self):
        self.kaa.register_resources('app', 'AppResources')

```

This class define your resources

```python
from kaa import GET, PATH, Resources, Response, Status


class AppResources(Resources):

    @GET
    @PATH('/')
    def basic_resource(self, **params):
        return Response(Status.OK).json({
            'message': 'your response'
        })

```


### Starting server
```
$ python app.py serve
```

By default host is 127.0.0.1 and port is 8086

Start with diferent host and port:
```
$ python app.py serve host:port
```
