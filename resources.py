import json

from kaa import resources
from kaa.decorators import GET, PATH
from kaa.enums import ContentType, Status
from kaa.request import Request
from kaa.response import Response


class Resources(resources.Resources):

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
