from django.db import models
from django.core.validators import MaxValueValidator
from config import constants


class Country(models.Model):
    name = models.CharField(max_length=64, blank=False)
    alpha_2 = models.CharField(max_length=2, primary_key=True)
    currencies = models.ManyToManyField('data.Currency',  related_name='currency_country')


class Currency(models.Model):
    name = models.CharField(max_length=128)
    alpha_3 = models.CharField(max_length=3, primary_key=True)


class Commodity(models.Model):
    name = models.CharField(max_length=64)
    symbol = models.CharField(max_length=32, null=True, blank=True)
    description = models.CharField(max_length=256, null=True, blank=True)
    group = models.CharField(max_length=21, choices=enumerate(constants.COMMODITY_GROUPS), null=True, blank=True)