from django.db import models
from config import constants


class Cryptocurrency(models.Model):
    name = models.CharField(max_length=64)
    symbol = models.CharField(max_length=32)
    url = models.CharField(max_length=256, null=True, blank=True)
    description = models.CharField(max_length=256, null=True, blank=True)
    hash_algorithm = models.CharField(max_length=64, null=True, blank=True)
    proof_type = models.CharField(max_length=32, null=True, blank=True)


class CryptoExchange(models.Model):
    name = models.CharField(max_length=128)
    grade = models.CharField(choices=enumerate(constants.CRYPTO_EXCHANGE_GRADES), max_length=3, null=True, blank=True)
    url = models.CharField(max_length=256, null=True, blank=True)
    countries = models.ManyToManyField('data.Country', related_name='exchange_countries', blank=True)
    currencies = models.ManyToManyField('data.Currency', related_name='exchange_currencies', blank=True)
    tickers = models.ManyToManyField('crypto.Cryptocurrency', related_name='exchange_tickers', blank=True)
    daily_vol = models.FloatField(null=True, blank=True)
    monthly_vol = models.FloatField(null=True, blank=True)




