from celery import Celery
from app.config import Config

celery_app = Celery('tasks', broker=Config.BROKER_URL, backend=Config.BACKEND_URL)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    broker_connection_retry_on_startup=True
)
