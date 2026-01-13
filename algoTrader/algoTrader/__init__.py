from .celery import app as celery_app

# This will ensure our app config is loaded
default_app_config = 'algoTrader.apps.AlgoTraderConfig'

__all__ = ('celery_app',)