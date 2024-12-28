from django.db import models


class CoverdCallOptions(models.Model):
    final_price_diff_percent_by_final_price = models.FloatField()
    cover_call_final_price_diff_percent_by_base_price = models.FloatField()
    symbol = models.CharField(max_length=30)
    original_symbol = models.CharField(max_length=30)
    end_date = models.DateField()
    delta = models.FloatField()
    highest_bid_price = models.IntegerField()
    lowest_ask_price = models.IntegerField()
    highest_bid_value = models.IntegerField()
    guarantee = models.IntegerField()
    original_symbol_lowest_ask_price = models.IntegerField()
    cover_call_final_price = models.IntegerField()  # 2200
    cover_call_volume = models.IntegerField()  # 1921
    cover_call = models.FloatField()  # 353464000
    cover_call_profit = models.FloatField()  # 132.5286309213951
    cover_call_in_end_date = models.FloatField()  # 51336000.0
    strick_price = models.FloatField()  # 51336000.0
    created_at = models.DateTimeField(auto_now_add=True)
    created_date_at = models.DateField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["created_date_at", "symbol"], name="nemidunam")
        ]




class CoverdCallDynamicConfig(models.Model):
    delta = models.FloatField(default=0.9)
    minimum_profit = models.FloatField(default=40)
    token = models.CharField(max_length=255, default="Bearer test")
