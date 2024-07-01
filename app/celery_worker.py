from app import create_app

app = create_app()
app.app_context().push()
from app.celery.celery_app import celery_app as celery

