from django.apps import AppConfig
import sys, os
import logging


logger = logging.getLogger(__name__)

class AlgoTraderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'algoTrader'

    def ready(self):
        # Log that we're attempting initialization
        logger.info("AlgoTraderConfig ready() method called")
        from celery import app
        
        
        # Prevent running twice in development server
        if os.environ.get('RUN_MAIN') != 'true' and 'runserver' in sys.argv:
            logger.info("Initializing Angel One service...")
            from .angel_one_services import AngelOneService
            try:
                # Get the singleton instance and ensure it's initialized
                service = AngelOneService.get_instance()
                # The service will automatically initialize and login in __init__
                logger.info("Angel One service initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Angel One service: {e}") 