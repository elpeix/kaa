import json

from kaa import GET, PATH, ContentType, Request, Response, Status, resources


class Resources(resources.Resources):

    @GET
    @PATH('')
    def baseResource(self):
        result = {
            "message": "Get resource /"
        }
        return Response(Status.OK).json(result)

    @GET
    @PATH('/resource/{id}/')
    def resourceWithId(self, id):
        result = {
            "queryParams": self.request.query,
            "status": "success",
            "id": id,
            "message": "Get resource /resource/{id}/"
        }
        return Response(Status.OK).json(result)

    @GET
    @PATH('/error')
    def errorResource(self):
        raise Exception("This is an error")
