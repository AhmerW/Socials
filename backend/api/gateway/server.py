from fastapi import FastAPI

import asyncpg


from gateway.resources.user import routes as user_routes
from common.create_app import createApp, createPool
from common import utils
from gateway.ctx import ServerContext as ctx


app = createApp()

@app.on_event('startup')
async def startup_event():
    ctx.pool = await createPool(
        {'server_settings': {'search_path': 'public'}},
        host='SERVER_DB_HOST',
        port='SERVER_DB_PORT',
        user='SERVER_DB_USER',
        password='SERVER_DB_PASSWD',
        database='SERVER_DB_DB'
    )


#dependencies = [] arg

app.include_router(user_routes.router, prefix='/user')
