from kaa.rest import Rest

def application(env, start_response):
    rest = Rest(env, start_response)
    return rest.serve({
        'rest.resources': 'Resources'
    })
