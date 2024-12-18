# Documentation

This project wants to provide an easy and fast REST interface development. It
is auto documented with OpenAPI spec (only routes).

## Requirements

There are no requirements.

- (Optional) `pyYAML` for YAML output in OpenAPI and other custom responses.
  Without it, OpenAPI defaults to JSON.

## Installation

### With PIP

```console
pip install kaa-rest-server
```

### Or source code

Download code from <https://github.com/elpeix/kaa>.

## Prepare server

### [Configuration](docs/configuration.md)

**kaa.json**: Specifies server handling.

```json
{
  "name": "My Server",
  "version": "1.0.0",
  "server": "server.MyServer",
  "debug": false,
  "enableCors": false,
  "developmentPolling": {
    "enabled": true,
    "intervalSeconds": 1,
    "include": [".", "src", "*.py"],
    "exclude": [
      "docs",
      "tests",
      "__pycache__",
      "*.md"
    ]
  }
}
```

See [Configuration](docs/configuration.md).

### Run server

#### CLI

```console
kaa serve
```

By default host is _localhost_ and port is _5321_.

You can define host and port in kaa.json or in console:

```console
kaa serve host:port
```

#### WSGI server

You can use **uswgi** or similar and call application method.

Requires a file with method named _application_.

```python
import importlib
from kaa.cli import Cli, Server

# For WSGI application
def application(env, start_response):
    return Server().serve(env, start_response)
```

Requires WSGI configuration. uWSGI:
<https://uwsgi-docs.readthedocs.io/en/latest/index.html>

## Server class

```python
from kaa import KaaServer

class Server(KaaServer):

    def register_resources(self):
        self.kaa.register_resources("resources", "AppResources")
```

This class initializes Kaa for each http request.

### Register resources

```python
register_resources(module: str, class_name: str)
```

This method registers classes with resources. _(view [Resources](#resources))_

### Register request filters

```python
register_filter_request(module: str, class_name: str)
```

This method registers classes with request filters. Each request it will pass
through these filters before enter to resource.

### Register response filters

This method registers classes with response filters. Each response it will pass
through these filters after resource (valid resources) and before return
response to client.

```python
from kaa import Kaa, KaaServer

class Server(KaaServer):

    def register_resources(self):
        self.kaa.register_resources("app", "appResources")
```

### Resources

```python
from kaa import GET, PATH, Resources, Response, Status

class AppResources(Resources):

    @GET
    @PATH("/")
    def basic_resource(self, **params):
        return Response(Status.OK).json({
            "message": "your response"
        })
```

You can create resource classes and register them at your _server_ class. This
classes must extend **Resource** from **kaa** module.

#### Path

Decorator @PATH

##### Argument uri

The argument _uri_ is required and identifies the uri path to which the resource
responds and is specified method of a resource. Uri path are uris with
variables. These variables are substituted in order to respond to a request
based on the substituted uri. Variables are denoted by braces (`{` and `}`).

Example:

```python
@PATH("/users/{username}")
# or
@PATH(uri="/users/{username}")
```

In this example, a user is prompted to type his or her name, and then Kaa
responds. For example, if the user types the user name “Mowgli,” the server
responds to the following URL:

`http://localhost:5321/users/Mowgli`

These uri variables allows create a simple regular expression to filter URL.

Example:

```python
@PATH("/books/{id:[0-9]}")
```

In this example, a id book must be a number.
The server does not respond to the following URL:

`http://localhost:5321/books/Mowgli`

But it responds to the following URL:

`http://localhost:5321/books/1`

##### Other arguments

**query_params**: Captures typed query params and pass them to resource method
as arguments.

Example:

```python
@GET
@PATH("/books",
      query_params={
         "max_results": {"type": "int", "default": 10},
         "page": {"type": "int", "default": 1}
     })
 def list_books(max_results, page):
    pass
```

In this example a list of books expects two params: _max_results_ and _page_.
Both are integers and have a default value.

Allowed types:

- int
- float
- str

If type is not defined param it will be a _str_.

When query param has a diferent type as its definition, it will be launch a
**400 Bad Request** response.

A query param can be required.

```python
@GET
@PATH("/books/search",
      query_params={
         "q": {"type": "string", "required": True},
         "max_results": {"type": "int", "default": 10},
         "page": {"type": "int", "default": 1}
     })
 def search_books(q, max_results, page):
    pass
```

In this exampla, query parama _q_ is required. If it is not passed, it will be
launch **400 Bad Request** response.

**path_params**: Only for OpenAPI documentation. Describe path params.

**description**: Only for OpenAPI documentation. Describe resource.

Example:

```python
@GET
@PATH("/writer/{id:[0-9]}/books",
      query_params={
         "max_results": {"type": "int", "default": 10},
         "page": {"type": "int", "default": 1}
     },
     description="Return a list of books from its writer",
     path_params={
         "id": {"type": "int", "description": "Identifier for a writer"}
     })
 def list_writer_books(id, max_results, page):
    pass
```

#### Methods

HTTP methods with decorator. They don't have arguments.

- **GET**
- **PUT**
- **POST**
- **PATCH**
- **DELETE**

#### Authorization

Decorator: @AUTH(AuthClass())

This decorators calls the class AuthClass. This class must extends
**Authorization** from _kaa_.

Example:

- Resource

```python
@POST
@AUTH(Auth())
@PATH("/book")
 def add_book(id):
    pass
```

- Auth class:

```python
class Auth(Authorization):

    def authorize(self, request:Request):
        if request.get_header("AUTHORIZATION") == "token":
            return True
        return False
```

## OpenAPI

`http://localhost:5321/openapi`

Returns OpenAPI response.

If PyYAML is installer,in **YAML** format.

You can get the response in **JSON** format with request header:
`Accept: application/json`.
