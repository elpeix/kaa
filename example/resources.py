from kaa import AUTH, DELETE, GET, PATCH, PATH, POST, PUT, Response, Status, resources

from .authorization import Auth


class Resources(resources.Resources):
    @GET
    @PATH(uri="/", query_params={"param": {"description": "Basic param"}})
    def base_resource(self, **params):
        result = {"message": "Get resource / with params: {}".format(params)}
        return Response(Status.OK).json(result)

    @GET
    @PATH(
        "/resource/{id}/",
        description="Resource with id",
        path_params={"id": {"type": "int", "description": "Identifier for resource"}},
        query_params={
            "rparam": {"type": "str", "required": True},
            "iparam": {"type": "int", "default": 42},
            "fparam": {"type": "float", "default": 1.0},
        },
    )
    def resource_with_id(self, id, rparam, iparam, fparam):
        result = {
            "queryParams": self.request.query,
            "status": "success",
            "id": id,
            "rparam": rparam,
            "iparam": iparam,
            "fparam": fparam,
            "message": "Get resource /resource/{id}/",
        }
        return Response(Status.OK).json(result)

    @GET
    @PATH("/error")
    def error_resource(self):
        raise Exception("This is an error")

    @GET
    @PATH("/authorize")
    @AUTH(Auth())
    def resource_auth(self):
        return Response(Status.OK).json({"message": "authorized"})

    @POST
    @PATH("/doPost")
    def resource_post(self):
        request_body = self.request.get_request_body()
        return Response(Status.OK).json({"message": "posted", "data": request_body})

    @PATCH
    @PATH("/doPatch")
    def resource_patch(self):
        request_body = self.request.get_request_body()
        return Response(Status.OK).json({"message": "patched", "data": request_body})

    @PUT
    @PATH("/doPut/{id}/")
    def resource_put(self, id):
        request_body = self.request.get_request_body()
        return Response(Status.OK).json(
            {"message": "put", "id": id, "data": request_body}
        )

    @DELETE
    @PATH("/doDelete/{id}/")
    def resource_delete(self, id):
        return Response(Status.OK).json({"message": "deleted", "id": id})
