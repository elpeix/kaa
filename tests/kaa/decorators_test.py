from kaa import Request, Resources
from tests.kaa.test_base import TestBase


class TestDecorators(TestBase):
    def get_resource(self, method="", path="path", q=""):
        request = Request(
            {
                "REQUEST_METHOD": method,
                "PATH_INFO": path,
                "REMOTE_ADDR": "127.0.0.1",
                "CONTENT_TYPE": "application/json",
                "QUERY_STRING": q,
            }
        )
        return Resources(request)
