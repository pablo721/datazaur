from django.db import models

# Create your models here.


class Client(models.Model):
	name = models.CharField(max_length=64)
	ip = models.CharField(max_length=64)
	user = models.ForeignKey('website.Account', on_delete=models.CASCADE, blank=True)


