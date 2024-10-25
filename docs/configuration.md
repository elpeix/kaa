# API Server Configuration

**kaa.json** defines settings for the API server, specifying core server
attributes, debugging options, CORS settings, and development polling. Adjust
these options to tailor server behavior for both production and development
environments.

## Configuration Fields

- **`name`** (string):  
  Defines the name of the server instance, which can be used in logging or
  identification purposes within the server’s ecosystem.
  - _Example_: `"name": "My Server"`
- **`version`** (string):  
  Specifies the version of the server or application. This field is useful for
  version control and managing deployment cycles.
  - _Example_: `"version": "1.0.0"`
- **`server`** (string):  
  Indicates the server class or module that serves as the entry point for the
  application. This should be the fully qualified name of the server class.
  - _Example_: `"server": "server.MyServer"`
- **`host`** (string):  
  Specifies the hostname or IP address where the server will run. Setting it to
  `"0.0.0.0"` allows the server to be accessible from any network interface on
  the host machine, making it suitable for local development or testing across
  devices on the same network. Defaut value: _localhost_.
  - _Example_: `"host": "0.0.0.0"` (accessible from any network)
  - _Example_: `"host": "127.0.0.1"` (only accessible from the local machine)
- **`port`** (integer):  
  Defines the port on which the server will listen for incoming requests. The
  port number should be an available, non-conflicting port on the machine.
  Defaut value: _5321_.
  - _Example_: `"port": 8080` (a common choice for development servers)
- **`debug`** (boolean):  
  Enables or disables debug mode. When set to `true`, the server show stack
  traces for errors, which is helpful during development. In production, it
  should be set to `false` to avoid exposing sensitive information.
  - _Example_: `"debug": false`
- **`enableCors`** (boolean):  
  Controls Cross-Origin Resource Sharing (CORS) for the API. When set to
  `true`, the server will allow requests from other origins, which is necessary
  if your API will be accessed from web applications hosted on different
  domains. For private APIs, this should generally be set to `false`.
  - _Example_: `"enableCors": false`

## Development Polling Configuration

The `developmentPolling` section is dedicated to monitoring file changes in
development mode. When enabled, this feature watches specified files and
directories for changes and automatically restarts the server to reflect
updates.

- **`enabled`** (boolean):  
  Enables or disables polling for file changes. Set this to `true` during
  development for automatic server restarts on file modifications.

  - _Example_: `"enabled": true`

- **`intervalSeconds`** (integer):  
  Defines how frequently (in seconds) the server checks for file changes. A
  shorter interval means faster updates but may slightly increase CPU usage.

  - _Example_: `"intervalSeconds": 1`

- **`include`** (array of strings):  
  Lists the files and directories to monitor. You can use glob patterns (`*.py`)
  to monitor specific file types or directory paths to watch entire folders.

  - _Examples_:
    - `.`: Includes the root directory.
    - `src`: Includes the `src` directory.
    - `*.py`: Monitors all Python files.

- **`exclude`** (array of strings):  
  Lists files and directories to exclude from polling. Patterns can be used to
  omit certain types of files or specific directories
  (e.g., `docs`, `tests`, `__pycache__`). This reduces unnecessary polling for
  files that do not impact development changes.
  - _Examples_:
    - `docs`: Excludes the `docs` directory.
    - `tests`: Excludes the `tests` directory.
    - `*.md`: Excludes all Markdown files.

## Example Configuration

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
    "exclude": ["docs", "tests", "__pycache__", "*.md"]
  }
}
```

This example sets up a server named _My Server_ running version `1.0.0` with
polling enabled for development. It monitors the root and `src` directories as
well as all Python files (`*.py`). Files in `docs`, `tests`, and `__pycache__`
olders, as well as Markdown files (`*.md`), are excluded from polling.
