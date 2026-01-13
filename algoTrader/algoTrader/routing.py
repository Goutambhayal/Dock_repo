from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'^ws/orders/$', consumers.OrderStatusConsumer.as_asgi()),
    re_path(r"ws/live-prices/$", consumers.LivePriceConsumer.as_asgi()),
    re_path(r"ws/trading-bot-data",consumers.TradingBotData.as_asgi()),
] 