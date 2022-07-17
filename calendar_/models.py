from django.db import models


class EconEvent(models.Model):
	id = models.IntegerField(primary_key=True, null=False, blank=False)
	date = models.DateField()
	time = models.TimeField()
	zone = models.CharField(max_length=16)
	currency = models.CharField(max_length=8)
	importance = models.CharField(max_length=16)
	title = models.CharField(max_length=128)
	actual = models.FloatField(null=True)
	forecast = models.FloatField(null=True)
	previous = models.CharField(max_length=16)


class CryptoEvent(models.Model):
	id = models.IntegerField(primary_key=True, null=False, blank=False)
	title = models.CharField(max_length=128)
	coins = models.CharField(max_length=128)
	date = models.DateTimeField()
	created_date = models.DateTimeField()
	categories = models.CharField(max_length=128)
	source = models.CharField(max_length=256)



