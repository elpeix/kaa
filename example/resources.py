import datetime
from kaa import (
    AUTH,
    DELETE,
    GET,
    PATCH,
    POST,
    PUT,
    Path,
    Produces,
    Response,
    Status,
    resources,
)
from kaa.enums import ContentType
from kaa.exceptions import ForbiddenError

from .authorization import Auth


class Resources(resources.Resources):
    @GET
    @Path(uri="/", query_params={"param": {"description": "Basic param"}})
    def base_resource(self, **params):
        result = {"message": f"Get resource / with params: {params}"}
        return Response(Status.OK).json(result)

    @GET
    @Path("/resource")
    @Produces(ContentType.JSON)
    def resource(self):
        result = {"message": "Get resource /resource"}
        return Response(Status.OK).of(result)

    @GET
    @Path(
        "/resource/{resource_id}/",
        description="Resource with id",
        path_params={"id": {"type": "int", "description": "Identifier for resource"}},
        query_params={
            "rparam": {"type": "str", "required": True},
            "iparam": {"type": "int", "default": 42},
            "fparam": {"type": "float", "default": 1.0},
        },
    )
    def resource_with_id(self, resource_id, rparam, iparam, fparam):
        result = {
            "queryParams": self.request.query,
            "status": "success",
            "id": resource_id,
            "rparam": rparam,
            "iparam": iparam,
            "fparam": fparam,
            "message": "Get resource /resource/{id}/",
            "someDate": datetime.datetime.now(),
        }
        return Response(Status.OK).json(result)

    @GET
    @Path("/error")
    @Produces(ContentType.JSON)
    def error_resource(self):
        raise ForbiddenError("This is an error")

    @GET
    @Path("/authorize")
    @Produces(ContentType.JSON)
    @AUTH(Auth())
    def resource_auth(self):
        return Response(Status.OK).json({"message": "authorized"})

    @POST
    @Path("/doPost")
    def resource_post(self):
        request_body = self.request.get_request_body()
        return Response(Status.OK).json({"message": "posted", "data": request_body})

    @PATCH
    @Path("/doPatch")
    def resource_patch(self):
        request_body = self.request.get_request_body()
        return Response(Status.OK).json({"message": "patched", "data": request_body})

    @PUT
    @Path("/doPut/{resource_id}/")
    def resource_put(self, resource_id):
        request_body = self.request.get_request_body()
        return Response(Status.OK).json(
            {"message": "put", "id": resource_id, "data": request_body}
        )

    @DELETE
    @Path("/doDelete/{resource_id}/")
    def resource_delete(self, resource_id):
        return Response(Status.OK).json({"message": "deleted", "id": resource_id})
