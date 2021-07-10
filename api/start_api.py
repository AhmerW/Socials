import os
import sys

import subprocess
from dotenv import load_dotenv
import uvicorn


from gateway.server import app
from common import utils

PYTHON_COMMAND = 'python'
DEFAULT_CMD = ['start', 'cmd', '/k']


SERVICE_CONFIG = {}

if __name__ == '__main__':
    load_dotenv('.env')
    _load_services = True
    args = [a for a in sys.argv[1::]]

    # Python services are not not loaded as an external process.
    # (Removed from SERVICE_CONFIG) too.

    for arg in args:
        if not arg.startswith('-'):
            continue
        arg, value = arg.split('=')
        arg = arg[1::]
        if arg == 'services':
            if value == 'false':
                _load_services = False

    # use something else than uvicorn for production (for the services, since they local)??
    if _load_services:
        for service in os.listdir('services'):
            if 'closed' in service:
                continue
            service_config = SERVICE_CONFIG.get(service)
            if not service_config:
                continue

            path = os.path.join(os.getcwd(), 'services', service, 'service.py')
            if os.path.isfile(path):
                if os.name == 'nt':
                    print('Starting service [', service, ']')
                    subprocess.call(
                        args=[
                            'start',
                            'cmd',
                            '/k',
                            PYTHON_COMMAND,
                            'service_launcher.py',
                            path,
                            service,
                            service_config['type']
                        ],
                        shell=True,
                    )
                    children = SERVICE_CONFIG[service].get('children')
                    if children:
                        for child in children:
                            subprocess.call(
                                args=child['cmd'],
                                **child['args']
                            )
                else:
                    print(os.name, 'not supported')

    """
    ONLY FOR DEVELOPMENT
    """

    uvicorn.run(app, host=utils.SERVER_IP, port=utils.SERVER_PORT)
