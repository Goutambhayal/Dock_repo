from django.db import models

# class Order(models.Model):
#     ORDER_STATUS = (
#         ('PENDING', 'Order Pending'),
#         ('PLACED', 'Order Placed'),
#         ('EXECUTED', 'Order Executed'),
#         ('REJECTED', 'Order Rejected'),
#         ('CANCELLED', 'Order Cancelled'),
#         ('ERROR', 'Error'),
#     )

#     ORDER_TYPES = (
#         ('PLACE', 'Place Order'),
#         ('EXIT', 'Exit Order'),
#         ('MODIFY', 'Modify Order'),
#     )

#     order_id = models.CharField(max_length=50, blank=True, null=True)  # Angel One order ID
#     task_id = models.CharField(max_length=50)  # Celery task ID
#     symbol = models.CharField(max_length=50)
#     quantity = models.IntegerField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     transaction_type = models.CharField(max_length=4)  # BUY or SELL
#     order_type = models.CharField(max_length=10, choices=ORDER_TYPES)
#     status = models.CharField(max_length=10, choices=ORDER_STATUS, default='PENDING')
#     error_message = models.TextField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering = ['-created_at']

#     def __str__(self):
#         return f"{self.transaction_type} {self.symbol} - {self.status}" 
# class intradayPrices(models.Model):
#     company_token = models.CharField(max_length=20)   # or IntegerField if numeric
#     price_time = models.DateTimeField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)

#     class Meta:
#         db_table = "Intraday_prices"   # so Django uses your existing table name
#         indexes = [
#             models.Index(fields=["company_token", "price_time"]),
#         ]

#     def __str__(self):
#         return f"{self.company_token} - {self.price} at {self.price_time}"
class all_companies(models.Model):
    company_name=models.CharField(max_length=35)
    symbol_name =models.CharField(max_length=20)
    symbol_token=models.CharField(max_length=20)
    market_capitalization = models.CharField(max_length=15)

    class Meta:
        db_table = "company_data"
    def __str__(self):
        return self.company_name
    
        