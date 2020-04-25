class Request():
    
    def __init__(self, env):
        self.env = env
        self.method = self.env['REQUEST_METHOD']
        self.path = self.env['PATH_INFO']
        self.remoteAddr = self.env['REMOTE_ADDR']
        self.query = self.__getQuery()
        self.headers = self.__getHeaders()

    def __getQuery(self):
        query = {}
        queryString = self.env['QUERY_STRING']
        if not queryString:
            return query
        for item in queryString.split('&'):
            values = item.split('=')
            query[values[0]] = values[1]
        return query
    
    def __getHeaders(self):
        headers = {}
        for item in self.env:
            if item[:5] == 'HTTP_':
               headers[item[5:]] = self.env[item]
        return headers
    
    def getHeader(self, key):
        if key in self.headers:
            return self.headers[key]
        return None

    def getDict(self):
        return {
            'method': self.method,
            'path': self.path,
            'remoteAddr': self.remoteAddr,
            'query': self.query,
            'headers': self.headers
        }
