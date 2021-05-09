from time import sleep
from celery import Celery
from common import utils

celery = Celery(
    'tasks',
    backend=f'redis://{utils.SERVICE_CHAT_REDIS_IP}:{utils.SERVICE_CHAT_REDIS_PORT}/0',
    broker=f'amqp://{utils.SERVICE_CHAT_RMQ_IP}:{utils.SERVICE_CHAT_RMQ_PORT}'
)



@celery.task
def celery_task(task: str) -> str:
    print(task)
    return f"test task returned {task}"
