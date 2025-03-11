from kaa import NotFoundError, Request, RequestFilter, Response, ResponseFilter


class OnRequest(RequestFilter):
    def filter(self, request: Request):
        if request.path == "/invalid":
            raise NotFoundError("Invalid resource")


class OnResponse(ResponseFilter):
    def filter(self, request: Request, response: Response):
        response.header("x-response", "anyResponse")


class EnableCors(ResponseFilter):
    def filter(self, request: Request, response: Response):
        if request.method == "OPTIONS":
            response.header("Access-Control-Allow-Origin", "http://localhost")
            response.header(
                "Access-Control-Allow-Headers",
                "X-Requested-With, Content-Type, Accept, Origin, Authorization",
            )
            response.header(
                "Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, PATCH, OPTIONS"
            )
