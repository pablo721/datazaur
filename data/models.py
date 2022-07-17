from django.db import models
from django.core.validators import MaxValueValidator
from config import constants


class Asset(models.Model):
    name = models.CharField(max_length=64)
    symbol = models.CharField(max_length=32, null=True, blank=True)
    description = models.CharField(max_length=256, null=True, blank=True)
    asset_class = models.CharField(max_length=16)


class Country(models.Model):
    name = models.CharField(max_length=64, blank=False)
    code = models.CharField(max_length=2, primary_key=True)
    currencies = models.ManyToManyField('data.Currency',  related_name='currency_country')


class Currency(models.Model):
    name = models.CharField(max_length=64)
    code = models.CharField(max_length=3, primary_key=True)
    description = models.CharField(max_length=256, null=True, blank=True)
    issuer = models.ForeignKey('data.Country', on_delete=models.CASCADE, related_name='currency_issuer', null=True)


class Commodity(models.Model):
    name = models.CharField(max_length=64)
    symbol = models.CharField(max_length=32, null=True, blank=True)
    group = models.CharField(max_length=21, choices=enumerate(constants.COMMODITY_GROUPS), null=True, blank=True)




