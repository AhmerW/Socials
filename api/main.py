import uvicorn


from gateway.server import app
from common import utils

app = app

if __name__ == '__main__':
    """
    ONLY FOR DEVELOPMENT
    """

    uvicorn.run("main:app", host=utils.SERVER_IP,
                port=utils.SERVER_PORT, reload=True)
