

from common.data.initialize import initializeConnections
from gateway.resources.ott import routes as ott_routes
from gateway.resources.user import routes as user_routes
from gateway.resources.chat import routes as chat_routes
from gateway.resources.message import routes as msg_routes
from gateway.resources.account import routes as account_routes

from common.response import ResponseModel, Success

from gateway import ctx
from gateway.ctx import app
from gateway.core.auth import auth


@app.on_event('startup')
async def startup_event():
    await initializeConnections()


@ app.on_event('shutdown')
async def shutdown_event():
    await ctx.producer.stop()


# Test endpoint
@ app.get('/', response_model=ResponseModel)
async def test_endpoint():
    return Success(
        detail='200!'
    )


# dependencies = [] arg

routers = {
    'ott': ott_routes,
    'user': user_routes,
    'chat': chat_routes,
    'message': msg_routes,
    'account': account_routes,
    'auth': auth
}

for prefix, routes in routers.items():
    assert hasattr(
        routes, 'router'), f'Missing concrete implementation of routes in {prefix}'

    app.include_router(
        getattr(
            routes,
            'router'
        ),
        prefix=f'/{prefix}'
    )
