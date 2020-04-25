from kaa.rest import Rest
from kaa.kaa import Kaa

def start_server():
    kaa = Kaa()
    kaa.registerFilterRequest('sample.filters', 'OnRequest')
    kaa.registerResources('sample.resources',  'Resources')
    kaa.registerFilterResponse('sample.filters', 'OnResponse')
    kaa.run()

start_server()
