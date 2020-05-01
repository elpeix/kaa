from kaa import Kaa


def application(env, start_response):
    kaa = Kaa(env, start_response)
    kaa.register_resources('sample.resources', 'Resources')
    kaa.register_filter_request('sample.filters', 'OnRequest')
    kaa.register_filter_response('sample.filters', 'OnResponse')
    kaa.register_filter_response('sample.filters', 'EnableCors')
    return kaa.serve()
