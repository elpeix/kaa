from kaa.decorators import GET, PATH
from kaa.view import View
from kaa.response import Response
from kaa.enums import Status, ContentType
import json

class Resources(View):

    def __init__(self):
        super().__init__()

    @GET
    @PATH('/resource/{id}/')
    def createLogiCommerce(self, id):
        result = {
            "request": self.request,
            "status": "success",
            "id": id,
            "message": "Get resource"
        }
        return Response(Status.OK).json(result)
