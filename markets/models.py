from django.db import models


class Ticker(models.Model):
    base = models.CharField(max_length=16)
    quote = models.CharField(max_length=16)
    bid = models.FloatField(blank=True, null=True)
    ask = models.FloatField(blank=True, null=True, default=0)
    daily_delta = models.FloatField(blank=True, null=True)
    daily_vol = models.FloatField(blank=True, null=True)
    daily_low = models.FloatField(blank=True, null=True)
    daily_high = models.FloatField(blank=True, null=True)



