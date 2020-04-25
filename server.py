from kaa.rest import Rest
from kaa.kaa import Kaa

def start_server():
    kaa = Kaa()
    kaa.registerFilterRequest(module='filters', className='OnRequest')
    kaa.registerResources(module='resources',  className='Resources')
    kaa.registerFilterResponse(module='filters', className='OnResponse')
    kaa.run()

start_server()