# Documentation Legacy

This file explains how start a Kaa server in legacy mode.

This mode will be removed in future versions.

## Installation

### With pip3

```bash
pip3 install kaa-rest-server
```

### Or source code

Download code from <https://github.com/elpeix/kaa>.

## Prepare server

### File definitions.py

**definition.py** provides the basic configuration for your server:

```python
import logging


NAME = 'Simple kaa Server'  # Your project name
VERSION = 'v1.0'  # Version
SERVER = 'app.Server'  # Module and main class

DEBUG = True
ENABLE_CORS = False

```

All this defined vars are required.

- **NAME**: Name of your project. It will be shown at openapi output.
- **VERSION**: Version of your project. It will be shown at openapi output.
- **SERVER**: defines module and class where is located your server definition.
- **DEBUG**: Debug mode will log all steps.
- **ENABLE_CORS**: It will check a request with OPTION method.
  CORS requires to create a _Response Filter_.

### File app.py

```python
import importlib

from kaa.cli import Cli, Server


# For uWSGI application
def application(env, start_response):
    return Server().serve(env, start_response)


# For development
if __name__ == "__main__":
    cli = Cli()
    cli.execute()

```

### Run server

#### CLI

```bash
python3 app.py serve
```

By default host is 127.0.0.1 and port is 5321

Start with diferent host and port:

```bash
python3 app.py serve host:port
```
