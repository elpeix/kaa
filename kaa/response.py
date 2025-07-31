import datetime
import json
import traceback

from .kaa_definition import KaaDefinition
from .enums import ContentType, Status
from .request import Request


class Response:
    def __init__(self, status: Status = Status.OK):
        self.response_body = None
        self.ready = False
        self.status = status
        self.headers = dict()
        self.set_content_type(ContentType.PLAIN)
        self.definitions = KaaDefinition()

    def body(self, response_body: str):
        self.response_body = str(response_body)
        self.ready = True
        return self

    def of(self, response: dict | str):
        self.response_body = response
        self.ready = not isinstance(response, dict)
        return self

    def html(self, html: str):
        self.set_content_type(ContentType.HTML)
        return self.body(json.dumps(html))

    def yaml(self, response: dict):
        try:
            import yaml

            self.set_content_type(ContentType.YAML)
            return self.body(yaml.dump(response))
        except ImportError:
            return self.body("YAML is not supported")

    def __json_serialize(self, response):
        if isinstance(response, (datetime.date, datetime.datetime)):
            return response.isoformat()
        raise TypeError(f"Type {type(response)} not serializable")

    def json(self, response: dict):
        self.set_content_type(ContentType.JSON)
        try:
            return self.body(json.dumps(response, default=self.__json_serialize))
        except Exception as e:
            return json.dumps(e)

    def get_status_code(self):
        return self.status.value[1]

    def set_content_type(self, content_type: ContentType):
        self.content_type = content_type
        self.header("Content-Type", content_type.value)

    def header(self, header_name, header_value):
        self.headers[header_name] = header_value
        return self

    def not_found(self, request: Request):
        self.status = Status.NOT_FOUND
        return self.__set_response(request, "Resource not found")

    def forbidden(self, request: Request):
        self.status = Status.FORBIDDEN
        self.response_body = "Forbidden"
        return self

    def server_error(self, request: Request, exc_info=None):
        self.status = Status.SERVER_ERROR
        data = {}
        if exc_info:
            if self.definitions.is_debug():
                data["exception"] = traceback.format_exception(*exc_info)
            else:
                self.definitions.log.error(self.status.value, exc_info=exc_info)
        return self.__set_response(request, "Internal server error", data)

    def __set_response(self, request: Request, message, data: dict = {}):
        if (
            request.get_header("ACCEPT") == "application/json"
            or request.get_force_accept() == ContentType.JSON
        ):
            self.json({"status": self.status.value[0], "message": message, **data})
        else:
            self.body(message + "\n" + str(data) if data else message)
        return self

    def get_response(self, accept: ContentType | None = None):
        content_type = self.__get_content_type(accept)
        if content_type == ContentType.JSON:
            return self.json(self.__get_dict_body())
        if content_type == ContentType.HTML:
            return self.html(str(self.response_body or ""))
        if content_type == ContentType.YAML:
            return self.yaml(self.__get_dict_body())
        return self.body(str(self.response_body or ""))

    def __get_content_type(self, accept: ContentType | None = None) -> ContentType:
        if self.content_type is not None and self.content_type != ContentType.PLAIN:
            return self.content_type
        if accept:
            return accept
        return ContentType.PLAIN

    def __get_dict_body(self) -> dict:
        if isinstance(self.response_body, dict):
            return self.response_body
        return {"data": self.response_body}
