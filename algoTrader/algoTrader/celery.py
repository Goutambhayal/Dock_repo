import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'algoTrader.settings')

app = Celery('algoTrader')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.worker_pool = "solo"

# Explicitly include the tasks module
app.conf.include = [
    'algoTrader.tasks',
    'algoTrader.strategy',
    'algoTrader.views',
]

# Auto-discover tasks in all installed apps
app.autodiscover_tasks()

# Optional: Configure Celery to use Redis as both broker and result backend
app.conf.broker_url = 'redis://localhost:6379/0'
#app.conf.result_backend = 'redis://localhost:6379/0'

# Add retry settings
app.conf.broker_connection_retry = True
app.conf.broker_connection_retry_on_startup = True

# Import your beat schedule from the separate file
from .cl_bt_schedule import CELERY_BEAT_SCHEDULE
app.conf.beat_schedule = CELERY_BEAT_SCHEDULE