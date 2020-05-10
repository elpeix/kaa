import os
import logging

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DEBUG = True
LOG = logging.getLogger()

NAME = 'Sample Server'
VERSION = 'v1.0'

SERVER = 'example.SampleServer'
ENABLE_CORS = True
