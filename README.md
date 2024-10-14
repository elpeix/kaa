# Kaa REST Server

A very simple python server framework for REST applications.

## Starting

### Requirements

- (optional) pyYaml for OpenApi output: It is not required.
  If it is not installed, OpenApi always returns a JSON response.

### Install

```bash
pip install kaa-rest-server
```

### Main files

#### Definitions (deprecated)

> [!WARNING]
> Deprecated. Use kaa.json to configure server

File definitions.py at the top of the project:

```python
import logging


NAME = 'Simple kaa Server'  # Your project name
VERSION = 'v1.0'  # Version
SERVER = 'server.MyServer'  # Module and main class

LOG = logging.getLogger()
DEBUG = True
ENABLE_CORS = False
```

#### kaa.json

New system to define basic configuration

```json
{
  "name": "My Server",
  "version": "1.0.0",
  "server": "server.MyServer",
  "basePath": ".",
  "debug": false,
  "enableCors": false
}
```

**basePath**: In dev mode. It is the path the system will look at to reload the server.

#### Main classes

(file server.py)

This class initializes Kaa for each http request

```python
from kaa import KaaServer

class Server(KaaServer):

    def register_resources(self):
        self.kaa.register_resources('resources', 'AppResources')
```

This class define your resources (resources.py)

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

#### Application file (optional)

Simple file to start server (app.py) **Optional**

You can call without app.py file:

```bash
kaa
```

```python
from kaa.cli import Cli, Server


# For WSGI application
def application(env, start_response):
    return Server().serve(env, start_response)


# For development
if __name__ == "__main__":
    cli = Cli()
    cli.execute()

```

### Starting server

```bash
kaa serve
```

(Old mode)

```bash
python app.py serve
```

Or (with auto reload)

```bash
kaa dev
```

(old mode)

```bash
python3 app.py dev
```

#### host and port

By default host is localhost and port is 8086

Start with different host and port:

Adding host and port on kaa.json file:

```json
{
  // ...
  "host": "localhost",
  "port": 1111
  // ...
}
```

Or in command line:

```bash
python app.py serve host:port
```
