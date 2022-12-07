## Concept

This project wants to provide an easy and fast REST interface development. It is auto documented with OpenAPI spec.

## Starting

### Requeriments

Kaa Rest Server needs PyYaml. It is necessary for openApi response.

### Installation

#### Via pip

You can install Kaa using pip command

```
pip install kaa-rest-server
```

#### Via source code

Download code from https://github.com/elpeix/kaa.


### Prepare server

#### Definition

This file, definition.py, provides the basic configuration for your server:

```python
import logging


NAME = 'Simple kaa Server'  # Your project name
VERSION = 'v1.0'  # Version 
SERVER = 'app.Server'  # Module and main class

LOG = logging.getLogger()
DEBUG = True
ENABLE_CORS = False

```

All this defined vars are required. 

- **NAME**: Name of your project. It will be shown at openapi output.
- **VERSION**: Version of your project. It will be shown at openapi output.
- **SERVER**: defines module and class where is located your server definition.
- **LOG**: Your log definition.
- **DEBUG**: Debug mode will log all steps.
- **ENABLE_CORS**: It will check a request with OPTION method. Cors requires to create a *Response Filter*.

#### app.Server

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

### Run server

#### Cli

```
$ python kaa.py serve
```

By default host is 127.0.0.1 and port is 8086

Start with diferent host and port:
```
$ python kaa.py serve host:port
```

#### WSGI server

You can use **uswgi** or similar and call application method.


## Application

This class initializes Kaa for each http request. (Cli uses one object)

#### Register resources

*register_resources (module: str, class_name: str)*

This method registers classes with resources. *(view [Resources](#Resources))*

#### Register request filters

*register_filter_request (module: str, class_name: str)*

This method registers classes with request filters. Each request it will pass through these filters before enter to resource. *(view [Filters](#Filters))*.

#### Register response filters

This method registers classes with response filters. Each response it will pass through these filters after resource (valid resources) and before return response to client. *(view [Filters](#Filters))*.

```python
from kaa import Kaa, KaaServer

class Server(KaaServer):
    
    def register_resources(self):
        self.kaa.register_resources('app', 'appResources')

```

### Resources

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

You can create resource classes and register them at your *server* class. This classes must extend **Resource** from **kaa** module.

#### Path
Decorator @PATH

##### Argument uri

The argument *uri* is required and identifies the uri path to which the resource responds and is specified method of a resource. Uri path are uris with variables. These variables are substituted in order to respond to a request based on the substituted uri. Variables are denoted by braces (`{` and `}`).

Example:

```python
@PATH("/users/{username}")
# or 
@PATH(uri="/users/{username}")
```

In this example, a user is prompted to type his or her name, and then Kaa responds. For example, if the user types the user name “Mowgli,” the server responds to the following URL:

```
http://example.com/users/Mowgli
```

These uri variables allows create a simple regular expression to filter URL.

Example:

```python
@PATH('/books/{id:[0-9]}')
```

In this example, a id book must be a number. The server does not respond to the following URL:

```
http://example.com/books/Mowgli
```

But it responds to the following URL:

```
http://example.com/books/1
```

##### Other arguments

**query_params**: Captures typed query params and pass them to resource method as arguments.

Example:

```python
@GET
@PATH('/books',
      query_params={
         'max_results': {'type': 'int', 'default': 10},
         'page': {'type': 'int', 'default': 1}
     })
 def list_books(max_results, page):
    pass
```

In this example a list of books expects two params: *max_results* and *page*. Both are integers and have a default value.

Allowed types:

- int
- float
- str

If type is not defined param it will be a *str*.

When query param has a diferent type as its definition, it will be launch a **400 Bad Request** response. 

A query param can be required.

```python
@GET
@PATH('/books/search',
      query_params={
         'q': {'type': 'string', 'required': True},
         'max_results': {'type': 'int', 'default': 10},
         'page': {'type': 'int', 'default': 1}
     })
 def search_books(q, max_results, page):
    pass
```

In this exampla, query parama *q* is required. If it is not passet, it will be launch **400 Bad Request** response.

**path_params**: Only for OpenAPI documentation. Describe path params.

**description**: Only for OpenAPI documentation. Describe resource.

Example:

```python
@GET
@PATH('/writer/{id:[0-9]}/books',
      query_params={
         'max_results': {'type': 'int', 'default': 10},
         'page': {'type': 'int', 'default': 1}
     },
     description='Return a list of books from its writer',
     path_params={
         'id': {'type': 'int', 'description': 'Identifier for a writer'}
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

This decorators calls the class AuthClass. This class must extends **Authorization** from *kaa*.

Example:

- Resource

```python
@POST
@AUTH(Auth())
@PATH('/book')
 def add_book(id):
    pass
```

- Auth class:

```python
class Auth(Authorization):

    def authorize(self, request:Request):
        if request.get_header('AUTHORIZATION') == 'token':
            return True
        return False
```



### Filters
TODO
### Response
TODO
### Request
TODO
### Exceptions
TODO

## Openapi

### Via cli
```
python kaa.py openapi
```

Prints open api response to console in **JSON** format.

### Via resource

```
http://example.com/openapi
```

Returns openapi response in **YAML** format.

You can get the response in **JSON** format with request header: *Accept: application/json*.

