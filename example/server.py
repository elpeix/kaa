from kaa import Kaa, KaaServer


class SampleServer(KaaServer):

    def get_kaa(self, env, start_response) -> Kaa:
        kaa = Kaa(env, start_response)
        kaa.register_resources('example.resources', 'Resources')
        kaa.register_filter_request('example.filters', 'OnRequest')
        kaa.register_filter_response('example.filters', 'OnResponse')
        kaa.register_filter_response('example.filters', 'EnableCors')
        return kaa
