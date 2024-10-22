from kaa import GET, PATH, Response, Status, Resources


class OtherResources(Resources):
    @GET
    @PATH("/other")
    def base_resource(self):
        result = {"message": "Get other resource"}
        return Response(Status.OK).json(result)
