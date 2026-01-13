import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
#from .models import Order
from asgiref.sync import async_to_sync,sync_to_async
from channels.layers import get_channel_layer
from .tasks import redis_client
r=redis_client

class OrderStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("order_updates", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("order_updates", self.channel_name)

    async def receive(self, text_data):
        pass  # We don't need to handle incoming messages for now

    async def order_update(self, event):
        """Send order update to WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'order_update',
            'order': event['order']
        }))

#    @database_sync_to_async
#     def get_order_status(self, order_id):
#         try:
#             order = Order.objects.get(id=order_id)
#             return {
#                 'id': order.id,
#                 'status': order.status,
#                 'symbol': order.symbol,
#                 'transaction_type': order.transaction_type,
#                 'price': str(order.price),
#                 'error_message': order.error_message,
#                 'updated_at': order.updated_at.strftime('%Y-%m-%d %H:%M:%S')
#             }
#         except Order.DoesNotExist:
#             return None

# def send_order_update(order_id):
#     """Helper function to send order updates to all connected clients"""
#     channel_layer = get_channel_layer()
#     order = Order.objects.get(id=order_id)
#     async_to_sync(channel_layer.group_send)(
#         "order_updates",
#         {
#             "type": "order_update",
#             "order": {
#                 'id': order.id,
#                 'status': order.status,
#                 'symbol': order.symbol,
#                 'transaction_type': order.transaction_type,
#                 'price': str(order.price),
#                 'error_message': order.error_message,
#                 'updated_at': order.updated_at.strftime('%Y-%m-%d %H:%M:%S')
#             }
#         })

# Create a sync redis client for sync_to_async usage.
#_redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

class LivePriceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "live_prices_group"
        # join the broadcast group (Celery/producer will send to this group)
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        # send an immediate snapshot from Redis so client doesn't wait for next publish
        initial = await sync_to_async(r.hgetall)('all_tokens')
        # convert string values to floats where possible
        initial_prices = {}
        for k, v in initial.items():
            try:
                initial_prices[k] = float(v)
            except Exception:
                # keep raw if parse fails
                initial_prices[k] = v

        await self.send(text_data=json.dumps({
            "type": "prices_snapshot",
            "prices": initial_prices
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # Called when a producer does group_send with type "prices_update"
    async def prices_update(self, event):
        """
        Expected event: {"type":"prices_update","prices":{token: price, ...},"ts": 123456789}
        """
        # just forward the prices dict to the client
        await self.send(text_data=json.dumps({
            "type": "prices_update",
            "prices": event.get("prices", {}),
        }))

class TradingBotData(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope.get("user")
        self.group_name = str(user.id)+user.client_code
        # join the broadcast group (Celery/producer will send to this group)
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept() 
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
    async def send_user_trades_data(self,event):
         # just forward the trades data  to the client
        await self.send(text_data=json.dumps({
            "type": "trades_data",
            "prices": event.get("trades", {}),
        }))