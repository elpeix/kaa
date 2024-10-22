from kaa import KaaServer


class SampleServer(KaaServer):
    def register_resources(self):
        self.kaa.register_resources("example.resources", "Resources")
        self.kaa.register_resources(
            "example.other_resources", "OtherResources")

    def register_filters(self):
        self.kaa.register_filter_request("example.filters", "OnRequest")
        self.kaa.register_filter_response("example.filters", "OnResponse")
        self.kaa.register_filter_response("example.filters", "EnableCors")
