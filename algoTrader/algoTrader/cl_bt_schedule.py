from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'insert-every-minute': {
        'task': 'algoTrader.tasks.insert_data_from_redis',
        'schedule': crontab(minute='*', hour='9-15'),
    },
    "run-watchdog-every-5-sec": {
        "task": "algoTrader.tasks.watchdog",
        "schedule": 30,  # every 5 second
    },
    "publish-live-prices-every-second": {
        "task": "algoTrader.tasks.publish_live_prices_snapshot",
        "schedule": 1.0,   # every 1 second (adjust as needed)
    },
    'update_price_fluctuation':{
        'task':'algoTrader.tasks.update_price_fluctuation',
        'schedule':crontab(minute='35', hour='15' ),
    },
    
}

