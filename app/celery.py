import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery("app")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.beat_schedule = {
    "run-every-30-minutes-check-mirrors": {
        "task": "healthcheck.tasks.task_schedule_all_mirrors",
        "schedule": 180.0,  # 30 minutes
    },
}

app.autodiscover_tasks()
