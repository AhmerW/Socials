from gateway.data.initialize import (
    closeConnections,
)
from common.settings.settings import SVC_DISPATCH_SETTINGS


from gateway.resources.ws import routes as ws_routes
from gateway.resources.ott import routes as ott_routes
from gateway.resources.users import routes as user_routes
from gateway.resources.chats import routes as chat_routes
from gateway.resources.messages import routes as msg_routes
from gateway.resources.notices import routes as notice_routes
from gateway.resources.account import routes as account_routes

from common.response import ResponseModel, Success

from gateway import ctx
from gateway.ctx import app
from gateway.core.auth import auth


# Test endpoint
@app.get("/", response_model=ResponseModel)
async def test_endpoint():
    return Success(detail="200!")


# dependencies = [] arg

routers = {
    "auth": auth,
    "ott": ott_routes,
    "users": user_routes,
    "chats": chat_routes,
    "messages": msg_routes,
    "notices": notice_routes,
    "account": account_routes,
}

for prefix, routes in routers.items():

    app.include_router(getattr(routes, "router"), prefix=f"/{prefix}")


if not SVC_DISPATCH_SETTINGS.IS_EXT:
    app.include_router(ws_routes.router, prefix="/ws")


# TODO implement permission scopes / intents
