import os

WEB_API_HOST = os.environ.get('WEB_API_HOST', 'localhost')
WEB_API_PORT = os.environ.get('WEB_API_PORT', 5000)

DB_API_HOST = os.environ.get('DB_API_HOST', 'localhost')
DB_API_PORT = os.environ.get('DB_API_PORT', 8001)

TELEMSG_API_HOST = os.environ.get('TELEMSG_API_HOST', 'localhost')
TELEMSG_API_PORT = os.environ.get('TELEMSG_API_PORT', 5001)
