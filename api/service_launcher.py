import os
import sys 
import importlib.util

import uvicorn

if __name__ == '__main__':
    if len(sys.argv) <= 2:
        print('Service path and service name required')
        sys.exit(0)
    path, service, type_ = sys.argv[1], sys.argv[2], sys.argv[3]
    if not os.path.isfile(path):
        print('Invalid service path')
        sys.exit(0)
            
    spec = importlib.util.spec_from_file_location("module.name", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if type_ == 'api':
        if os.name == 'nt':
            os.system(f'title {service}')
        uvicorn.run(
            module.app,
            host=module.HOST,
            port=module.PORT
            
        )
    elif type_ == 'cls':
        module.main()