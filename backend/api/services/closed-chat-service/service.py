import os


from fastapi import FastAPI, BackgroundTasks
import uvicorn
import asyncpg


from common.create_app import createApp
from common import utils
from services.chat_service import models
from services.chat_service.ctx import ServiceContext as ctx

from services.chat_service.worker import worker


app = createApp(title='Chat-Service')

HOST = utils.SERVICE_CHAT_IP
PORT = utils.SERVICE_CHAT_PORT


@app.on_event('startup')
async def startup_event():
    pass


@app.get('/send')
async def chatSend(word: str):
    #if not data.type_ in models.message_types:
        #return {'ok': False}   
    worker.celery_task.delay(word)
    return {'ok': True}

