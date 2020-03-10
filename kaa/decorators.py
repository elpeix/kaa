import re
from kaa.response import Response
from kaa.enums import ContentType, Status
from kaa.authorization import Authorization


def AUTH(auth:Authorization):
    def decoratorPath(func):
        def wrapper(self, **kwargs):
            if auth.authorize(self.request):
                return func(self, **kwargs)
            return auth.forbidden(self.request)
        return wrapper
    return decoratorPath

def GET(func):
    def wrapper(self, **kwargs):
        if self.request.method == 'GET':
            return func(self, **kwargs)
    return wrapper

def POST(func):
    def wrapper(self, **kwargs):
        if self.request.method == 'POST':
            return func(self, **kwargs)
    return wrapper

def PUT(func):
    def wrapper(self, **kwargs):
        if self.request.method == 'PUT':
            return func(self, **kwargs)
    return wrapper

def DELETE(func):
    def wrapper(self, **kwargs):
        if self.request.method == 'DELETE':
            return func(self, **kwargs)
    return wrapper

def PATH(url):
    def decoratorPath(func):
        def wrapper(self):
            requestPath = self.request.path.strip("/")
            definedPath = url.strip("/")

            if requestPath == definedPath:
                return func(self)

            splitRequestPath = requestPath.split('/')
            splitDefinedPath = definedPath.split('/')

            if (len(splitRequestPath) != len(splitDefinedPath)):
                return

            # pathRegexp = r'\/((\{([a-z][a-zA-Z0-9_]+(:[^}]+){0,1})+\}|[a-zA-Z0-9_]+)\/?)*\/?'
            valueRegexp = r'^\{([a-z_][a-zA-Z0-9_]+)(:[^}]+){0,1}\}$'
            arguments = dict()
            for i in range(len(splitDefinedPath)):
                if splitDefinedPath[i] == splitRequestPath[i]:
                    continue
                m = re.search(valueRegexp, splitDefinedPath[i])

                if m is None:
                    return

                if m.group(2):
                    pattern = re.compile(m.group(2)[1:])
                    n = re.search(pattern, splitRequestPath[i])
                    if (n is None):
                        return
                arguments[m.group(1)] = splitRequestPath[i]          

            return func(self, **arguments)
        return wrapper
    return decoratorPath