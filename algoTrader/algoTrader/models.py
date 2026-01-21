from django.db import models
    
class ChartPriceData(models.Model):
    company_token = models.CharField(max_length=20)
    price_time = models.TimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "chart_price_data"
        constraints = [
            models.UniqueConstraint(
                fields=["company_token", "price_time"],
                name="unique_company_time"
            )
        ]

    def __str__(self):
        return f"{self.company_token} @ {self.price_time} = {self.price}"

class CompanyData(models.Model):
    company_name = models.CharField(max_length=70,null=True)
    symbol_name = models.CharField(max_length=30,null=True)
    symbol_token = models.CharField(max_length=20)
    market_capitalization = models.CharField(max_length=30)
    initial_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    last_day_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )


    class Meta:
        db_table = "company_data"

    def __str__(self):
        return f"{self.company_name} ({self.symbol_name})"




class PriceFluctuationData(models.Model):
    date = models.DateField()
    token = models.CharField(max_length=20)

    initial_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    g_up_h = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    g_up_l = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    up_gap = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    g_down_h = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    g_down_l = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    down_gap = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    final_percent_gain = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )

    d_high = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    d_low = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        db_table = "price_fluctuation_data"
        constraints = [
            models.UniqueConstraint(
                fields=["date", "token"],
                name="unique_price_fluctuation_date_token"
            )
        ]

    def __str__(self):
        return f"{self.token} | {self.date}"
