from kaa import Kaa, KaaServer


class SampleServer(KaaServer):

    def register_resources(self):
        self.kaa.register_resources('example.resources', 'Resources')

    def register_filters(self):
        self.kaa.register_filter_request('example.filters', 'OnRequest')
        self.kaa.register_filter_response('example.filters', 'OnResponse')
        self.kaa.register_filter_response('example.filters', 'EnableCors')
