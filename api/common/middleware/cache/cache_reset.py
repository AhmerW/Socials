from functools import wraps
import json

from starlette.responses import JSONResponse


def call_after(only_on_success, callback):
    """"Calls after the request is finished"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            resp = await func(*args, **kwargs)
            try:
                raw = json.loads(resp.body)

                if only_on_success and not raw.get('ok') is True:
                    return resp

                await callback(kwargs.get('request'))
            except json.JSONDecodeError:
                pass

            return resp
        return wrapper
    return decorator
