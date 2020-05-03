from kaa import Kaa, KaaServer


class SampleServer(KaaServer):

    def get_kaa(self, env, start_response) -> Kaa:
        kaa = Kaa(env, start_response)
        kaa.register_resources('sample.resources', 'Resources')
        kaa.register_filter_request('sample.filters', 'OnRequest')
        kaa.register_filter_response('sample.filters', 'OnResponse')
        kaa.register_filter_response('sample.filters', 'EnableCors')
        return kaa

    def generate_openapi(self):
        return dict()
