from django.db import models
from data.models import Asset



class Ticker(models.Model):
    base_asset_class = models.CharField(max_length=32, null=True, blank=True)
    base = models.CharField(max_length=16)
    base_full_name = models.CharField(max_length=128, blank=True, null=True)
    quote_asset_class = models.CharField(max_length=32, null=True, blank=True)
    quote = models.CharField(max_length=16)
    quote_full_name = models.CharField(max_length=128, blank=True, null=True)


class Quote(models.Model):
    ticker = models.ForeignKey('markets.Ticker', related_name='ticker_quote', on_delete=models.CASCADE)
    bid = models.FloatField(blank=True, null=True)
    ask = models.FloatField(blank=True, null=True, default=0)
    timestamp = models.DateTimeField()
    source = models.CharField(max_length=64)
    daily_delta = models.FloatField(blank=True, null=True)
    daily_pct_delta = models.FloatField(blank=True, null=True)
    daily_vol = models.FloatField(blank=True, null=True)
    daily_low = models.FloatField(blank=True, null=True)
    daily_high = models.FloatField(blank=True, null=True)




