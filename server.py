from kaa import Kaa


def application(env, start_response):
    kaa = Kaa(env, start_response)
    kaa.registerResources('sample.resources', 'Resources')
    kaa.registerFilterRequest('sample.filters', 'OnRequest')
    kaa.registerFilterResponse('sample.filters', 'OnResponse')
    kaa.registerFilterResponse('sample.filters', 'EnableCors')
    return kaa.serve()
