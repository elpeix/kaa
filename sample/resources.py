import json

from kaa import GET, PATH, Response, Status, resources


class Resources(resources.Resources):

    @GET
    @PATH('', query_params={'param': {}})
    def base_resource(self, **params):
        result = {
            "message": "Get resource / with params: {}".format(params)
        }
        return Response(Status.OK).json(result)

    @GET
    @PATH('/resource/{id}/',
          query_params={
              'rparam': {'type': 'str', 'required': True},
              'iparam': {'type': 'int', 'default': 42}
          })
    def resource_with_id(self, id, rparam, iparam):
        result = {
            "queryParams": self.request.query,
            "status": "success",
            "id": id,
            "rparam": rparam,
            "iparam": iparam,
            "message": "Get resource /resource/{id}/"
        }
        return Response(Status.OK).json(result)

    @GET
    @PATH('/error')
    def error_resource(self):
        raise Exception("This is an error")
