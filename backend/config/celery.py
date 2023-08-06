from celery import Celery
import os


celery = Celery("config")


# Pytest sets TASK_ALWAYS_EAGER env variable for testing purposes.
if os.environ.get('TASK_ALWAYS_EAGER'):
    # while testing, tasks wont be executed on workers.
    celery.conf.task_always_eager = True


celery.config_from_object("django.conf:settings", namespace="CELERY")
celery.autodiscover_tasks()