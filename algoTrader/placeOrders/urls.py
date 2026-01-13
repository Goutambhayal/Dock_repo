from django.urls import path
from . import views
from .auto_trading import start_trading
from . import auto_trading

urlpatterns = [
    # path('', views.home, name='home'),  # Example URL
    path("top_30_last_day_gainers/", views.top_30_last_day_gainers, name="top_30_last_day_gainers"),
    path("top_30_last_day_losers/",views.top_30_last_day_losers ,name="top_30_last_day_losers"),
    path("last-day-gainers/", views.last_day_gainers, name="last_day_gainers"),
    path("news/", views.news, name="news"),
    path("company_data",views.companies_data, name="company_data"),
    path("trading-bot/", views.trading_bot,name="trading_bot"),
    path('start-trading/', start_trading.as_view(), name='start_trading'),
    path('check-credential',auto_trading.check_credentials,name='check_credentials'),
    path('deactivate/',auto_trading.deactivate,name='deactivate'),
    ]